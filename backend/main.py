"""
FastAPI Backend Server — orchestrates PDF parsing, RAG retrieval, AI generation, and pricing.
Provides both synchronous and SSE streaming endpoints.
"""

import asyncio
import json
import os
import time
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pdf_processor import extract_text_from_pdf
from db_query import query_similar_projects, extract_keywords
from ai_generator import generate_proposal, HAS_API_KEY
from pricing_engine import calculate_pricing

app = FastAPI(
    title="Proposal Generator API",
    description="Automated Technical Proposal & Bid Generator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "llm_configured": HAS_API_KEY,
        "mode": "live" if HAS_API_KEY else "mock",
    }


@app.post("/api/generate")
async def generate(file: UploadFile = File(...)):
    """
    Full proposal generation — accepts a PDF, returns a complete proposal with pricing.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        # Step 1: Parse PDF
        file_bytes = await file.read()
        extracted_text = extract_text_from_pdf(file_bytes)

        if not extracted_text or len(extracted_text.strip()) < 20:
            raise HTTPException(status_code=400, detail="Could not extract meaningful text from the PDF.")

        # Step 2: RAG query
        similar_projects = query_similar_projects(extracted_text)

        # Step 3: AI generation
        proposal = generate_proposal(extracted_text, similar_projects)

        # Step 4: Deterministic pricing
        pricing = calculate_pricing(proposal.get("milestones", []))

        return {
            "success": True,
            "proposal": proposal,
            "pricing": pricing,
            "rag_context": {
                "matched_projects": len(similar_projects),
                "projects": [
                    {"title": p["title"], "type": p["project_type"], "relevance": p.get("relevance_score", 0)}
                    for p in similar_projects
                ],
            },
            "metadata": {
                "source_file": file.filename,
                "extracted_text_length": len(extracted_text),
                "mode": "live" if HAS_API_KEY else "mock",
            },
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response as JSON. Please try again.")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@app.post("/api/generate-stream")
async def generate_stream(file: UploadFile = File(...)):
    """
    SSE streaming endpoint — sends real-time processing status updates
    followed by the final proposal payload.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    file_bytes = await file.read()

    async def event_stream():
        try:
            # Step 1: Parse PDF
            yield _sse_event("status", {
                "step": "parsing",
                "message": f"📄 Parsing PDF: {file.filename}...",
                "progress": 10,
            })
            await asyncio.sleep(0.5)

            extracted_text = extract_text_from_pdf(file_bytes)

            if not extracted_text or len(extracted_text.strip()) < 20:
                yield _sse_event("error", {"message": "Could not extract meaningful text from the PDF."})
                return

            yield _sse_event("status", {
                "step": "parsed",
                "message": f"✅ Extracted {len(extracted_text)} characters from PDF",
                "progress": 25,
            })
            await asyncio.sleep(0.3)

            # Step 2: Extract keywords & RAG query
            yield _sse_event("status", {
                "step": "rag_query",
                "message": "🔍 Querying RAG database for similar projects...",
                "progress": 35,
            })
            await asyncio.sleep(0.5)

            keywords = extract_keywords(extracted_text)
            similar_projects = query_similar_projects(extracted_text)

            yield _sse_event("status", {
                "step": "rag_results",
                "message": f"📊 Found {len(similar_projects)} relevant historical project(s) | Keywords: {', '.join(keywords[:8])}",
                "progress": 45,
            })
            await asyncio.sleep(0.3)

            for p in similar_projects:
                yield _sse_event("status", {
                    "step": "rag_match",
                    "message": f"  ↳ Match: {p['title']} (Score: {p.get('relevance_score', '?')})",
                    "progress": 48,
                })
                await asyncio.sleep(0.2)

            # Step 3: AI generation
            mode = "Gemini LLM" if HAS_API_KEY else "Mock Engine"
            yield _sse_event("status", {
                "step": "ai_generating",
                "message": f"🤖 Generating proposal via {mode}...",
                "progress": 55,
            })
            await asyncio.sleep(0.5)

            proposal = generate_proposal(extracted_text, similar_projects)

            yield _sse_event("status", {
                "step": "ai_complete",
                "message": f"✅ AI generated {len(proposal.get('milestones', []))} milestones & {len(proposal.get('tech_stack', []))} tech recommendations",
                "progress": 75,
            })
            await asyncio.sleep(0.3)

            # Step 4: Pricing
            yield _sse_event("status", {
                "step": "pricing",
                "message": "💰 Calculating deterministic pricing matrix...",
                "progress": 85,
            })
            await asyncio.sleep(0.5)

            pricing = calculate_pricing(proposal.get("milestones", []))

            yield _sse_event("status", {
                "step": "pricing_complete",
                "message": f"✅ Priced at ${pricing['grand_total']:,} USD ({pricing['subtotal_hours']} total hours)",
                "progress": 95,
            })
            await asyncio.sleep(0.3)

            # Final result
            yield _sse_event("status", {
                "step": "complete",
                "message": "🚀 Proposal generation complete!",
                "progress": 100,
            })
            await asyncio.sleep(0.2)

            yield _sse_event("result", {
                "success": True,
                "proposal": proposal,
                "pricing": pricing,
                "rag_context": {
                    "matched_projects": len(similar_projects),
                    "projects": [
                        {"title": p["title"], "type": p["project_type"], "relevance": p.get("relevance_score", 0)}
                        for p in similar_projects
                    ],
                },
                "metadata": {
                    "source_file": file.filename if hasattr(file, 'filename') else "uploaded.pdf",
                    "extracted_text_length": len(extracted_text),
                    "mode": "live" if HAS_API_KEY else "mock",
                },
            })

        except Exception as e:
            traceback.print_exc()
            yield _sse_event("error", {"message": f"Processing error: {str(e)}"})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


def _sse_event(event_type: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
