# 03. 앱 구현 — nashsu/llm_wiki

Karpathy의 추상 패턴을 **크로스 플랫폼 데스크톱 앱**(Tauri v2)으로 구현하고 대폭 확장했다. 원본의 3계층·3대 작업·index/log·[[wikilink]]·YAML frontmatter·Obsidian 호환·역할 분담을 충실히 유지한다.

## 2단계 Chain-of-Thought 인제스트

원본의 단일 단계(읽기+쓰기 동시)를 품질을 위해 **두 번의 순차 LLM 호출**로 분리:

1. **분석** — 소스를 읽고 구조화 분석(핵심 엔티티·개념·주장, 기존 위키와의 연결, 모순/긴장, 구조 권장).
2. **생성** — 분석을 받아 위키 파일 생성(frontmatter 포함 소스 요약, 상호 참조 엔티티·개념 페이지, index/log/overview 갱신, 리뷰 항목, Deep Research 쿼리).

추가: SHA256 증분 캐시(미변경 파일 스킵), 영속 인제스트 큐(직렬·재시도 3회), 폴더 가져오기, 소스 폴더 자동 감시, 출처 추적성(`sources: []`).

## 지식 그래프

**4-신호 관련성 모델**: 직접 링크(×3.0), 출처 중복(×4.0), Adamic-Adar(×1.5), 타입 친화도(×1.0). 시각화는 sigma.js + graphology + ForceAtlas2.

**Louvain 커뮤니티 감지**로 지식 클러스터 자동 발견 + 응집도 점수(< 0.15는 경고).

**그래프 인사이트**: 뜻밖의 연결(교차 커뮤니티/타입 엣지), 지식 공백(고립 페이지·희소 커뮤니티·브리지 노드) → 한 클릭 Deep Research.

## 검색 파이프라인 (Query)

1. **토큰화 검색**(영어 단어분리/중국어 CJK bigram, 제목 일치 보너스)
2. **벡터 의미 검색(선택)** — OpenAI 호환 임베딩 + LanceDB. recall 58.2% → 71.4%.
3. **그래프 확장** — 상위 결과를 seed로 4-신호 2-hop 탐색.
4. **예산 제어** — context window 4K~1M, 비례 할당(Wiki 60 / chat 20 / index 5 / system 15).

## 생태계

- **Deep Research** — Tavily/SerpApi/SearXNG 다중 쿼리 웹 검색 → 결과를 위키에 자동 인제스트.
- **Chrome Web Clipper**(Manifest V3) — Readability.js + Turndown.js로 웹→마크다운, 자동 인제스트.
- **로컬 HTTP API(127.0.0.1:19828) + MCP Server + Agent Skill** — Claude Code/Codex가 하이브리드 검색·파일 읽기·그래프 탐색을 수행. `npx skills add ...` 한 줄 설치.
- **purpose.md** — 위키가 "왜" 존재하는지(목표·핵심 질문·논지). schema(구조 규칙)와 구분되는 방향성 의도.
- **Obsidian 호환** — 위키 디렉토리를 vault로 사용. 비동기 Review(Human-in-the-Loop), KaTeX, 다중 대화.

## 기술 스택

| 계층 | 기술 |
|------|------|
| Desktop | Tauri v2 (Rust) |
| Frontend | React 19 + TypeScript + Vite |
| UI | shadcn/ui + Tailwind v4 |
| Graph | sigma.js + graphology + ForceAtlas2 |
| Vector DB | LanceDB (선택) |
| 문서 | pdf-extract, docx-rs, calamine, 선택적 MinerU |
| LLM | OpenAI · Anthropic · Google · Ollama · Custom |
| Web Search | Tavily · SerpApi · SearXNG |
