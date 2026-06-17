# Development Concept AI Chatbot

Llama 3.2 3B Base 모델을 기반으로 Multi-Stage QLoRA Fine-Tuning을 적용하여 개발 개념 설명에 특화된 AI 챗봇을 구축한 프로젝트입니다.

웹 UI와 Flask API 서버를 구현하고 AWS 환경에 배포하여 실제 서비스 형태로 제공하는 것을 목표로 개발했습니다.

---

# Project Overview

기존 범용 LLM은 일반적인 질문에는 높은 성능을 보이지만 개발 개념 설명에서는 답변 구조가 일정하지 않거나 설명의 깊이가 부족한 경우가 있었습니다.

본 프로젝트는 이러한 문제를 해결하기 위해 개발 개념 설명에 특화된 데이터셋을 구축하고 Multi-Stage QLoRA 학습을 통해 한국어 기반 개발 개념 설명 챗봇을 구현했습니다.

## Goals

* 개발 개념 설명 특화 AI 구축
* 한국어 응답 품질 향상
* 웹 서비스 형태 제공
* AWS 기반 배포 환경 구축

---

# System Architecture

```text
User
 │
 ▼
Web UI
 │
 ▼
AWS Web Server
 │
 ▼
Flask API Gateway
 │
 ▼
Inference Server
 │
 ▼
Fine-Tuned Llama 3.2
```

## Architecture Design

* Web Server와 Inference Server 역할 분리
* 유지보수성 향상
* 모델 교체 및 확장 용이
* GPU 비용 절감

---

# Tech Stack

## AI

* Llama 3.2 3B Base
* QLoRA
* PEFT
* TRL
* Transformers

## Backend

* Flask
* Flask-RESTX

## Frontend

* HTML
* CSS
* JavaScript

## Infrastructure

* AWS EC2
* Ngrok

## Monitoring

* TensorBoard

---

# Multi-Stage QLoRA Pipeline

```text
Llama 3.2 Base
      │
      ▼
Phase 1
(KoAlpaca)
      │
      ▼
Phase1 Merged
      │
      ▼
Phase 2
(Development Dataset)
      │
      ▼
Phase2 Merged
      │
      ▼
Production Model
```

## Phase 1

목적

* 한국어 응답 품질 향상

데이터셋

* KoAlpaca

---

## Phase 2

목적

* 개발 개념 설명 특화

데이터셋

* 자료구조
* 알고리즘
* 운영체제
* 네트워크
* 데이터베이스
* C#

---

# Dataset Design

개발 질문에 대해 일관된 응답을 생성하도록 다음 구조를 기준으로 데이터셋을 설계했습니다.

```text
정의
동작 방식
장점
단점
사용 예시
```

예시 질문

```text
Queue란 무엇인가?
```

예시 응답

```text
정의
Queue는 FIFO 구조를 가지는 자료구조입니다.

동작 방식
먼저 들어온 데이터가 먼저 제거됩니다.

장점
...
```

---

# API Design

## Request

POST /chat

```json
{
  "prompt": "Queue가 뭐야?"
}
```

## Response

```json
{
  "response": "..."
}
```

---

# Key Challenges

## GPU Memory Limitation

### Problem

학습 과정에서 GPU 메모리 부족으로 인해 Out Of Memory 오류가 발생했습니다.

### Solution

* QLoRA 적용
* 4bit Quantization
* Gradient Accumulation 적용

### Result

제한된 GPU 환경에서도 안정적인 학습이 가능하도록 개선했습니다.

---

## Response Quality Issue

### Problem

일반 질문에도 개발 설명 형식이 출력되는 문제가 발생했습니다.

### Cause

개발 데이터 편중

### Solution

* 일반 대화 데이터 추가
* 데이터 비율 조정

### Result

질문 유형에 따라 적절한 응답 생성

---

# Results

* Multi-Stage QLoRA 학습 파이프라인 구축
* 개발 개념 특화 모델 구현
* Flask 기반 REST API 구축
* AWS 배포 환경 구성
* 웹 기반 챗봇 서비스 구현

---

# Future Improvements

* 데이터셋 확대
* 자동 평가 시스템 구축
* RAG 적용
* LangChain 적용
* LangGraph 기반 Workflow 설계

---

# Demo

프로젝트 화면

![chatbot](docs/chatbot.png)

---

# Author

박준수

AI Engineer / Software Developer
