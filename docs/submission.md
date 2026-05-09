# SHL Submission Document

## Project Title
AI-Powered SHL Assessment Recommendation Chatbot

## Problem Solved
Converts recruiter hiring requirements into ranked SHL assessment recommendations through conversational querying with context memory.

## Core Features Delivered
1. Conversational chatbot
2. Follow-up questions for missing context
3. Top-3 ranked recommendations
4. Hybrid matching: keyword + semantic overlap
5. Confidence score per recommendation
6. Structured JSON API (`POST /chat`)
7. Conversation history retention
8. Hallucination guardrails via fixed local catalog

## Technical Stack
- Backend: Flask
- Frontend: HTML/CSS/JS
- Data: JSON
- Deploy: Render

## Evaluation Alignment
- Problem solving: clear modular architecture
- Programming: clean and testable Python modules
- Context engineering: clarification + memory-driven ranking
- Agent behavior: ask, retrieve, recommend with strict constraints
