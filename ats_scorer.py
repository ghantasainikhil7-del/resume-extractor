import re

# Standard High-Impact Action Verbs preferred by ATS & Recruiters
ACTION_VERBS = [
    "accelerated", "accomplished", "achieved", "administered", "advanced",
    "analyzed", "architected", "automated", "built", "championed", "collaborated",
    "consolidated", "constructed", "coordinated", "created", "decreased", "delivered",
    "deployed", "designed", "developed", "devised", "directed", "eliminated",
    "engineered", "enhanced", "established", "executed", "expanded", "expedited",
    "formulated", "founded", "generated", "guided", "implemented", "improved",
    "increased", "initiated", "innovated", "installed", "instituted", "integrated",
    "introduced", "launched", "lead", "led", "managed", "maximized", "mentored",
    "migrated", "minimized", "modernized", "negotiated", "operated", "optimized",
    "orchestrated", "organized", "overhauled", "pioneered", "planned", "produced",
    "programmed", "reduced", "reengineered", "resolved", "revamped", "scaled",
    "simplified", "spearheaded", "standardized", "streamlined", "strengthened",
    "structured", "supervised", "surpassed", "trained", "transformed", "upgraded"
]

# Standard Resume Section Keywords
SECTION_PATTERNS = {
    "Contact & Personal Details": r"(?:email|phone|contact|address|linkedin|github)",
    "Professional Summary / Objective": r"(?:summary|objective|profile|about\s+me|professional\s+summary)",
    "Work Experience / History": r"(?:experience|employment|work\s+history|professional\s+experience|career)",
    "Technical Skills & Competencies": r"(?:skills|technical\s+skills|core\s+competencies|technologies|proficiencies)",
    "Education & Academics": r"(?:education|academic|degree|university|college|bachelor|master|phd|b\.tech|m\.tech|b\.e|b\.s|m\.s)",
    "Projects & Achievements": r"(?:projects|personal\s+projects|academic\s+projects|achievements|key\s+accomplishments|publications)"
}

# Target Job Profiles and Authoritative Required Skills Benchmark
JOB_PROFILES = {
    "AI / Machine Learning Engineer": {
        "required_skills": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "computer vision", "docker", "git"],
        "bonus_skills": ["kubernetes", "aws", "mlops", "scikit-learn", "numpy", "pandas", "rest api", "linux"],
        "description": "Develops production-ready neural networks, predictive models, distributed training pipelines, and LLM/NLP architectures."
    },
    "Full Stack Software Engineer": {
        "required_skills": ["javascript", "typescript", "react", "node.js", "python", "sql", "git", "html", "css"],
        "bonus_skills": ["docker", "postgresql", "mongodb", "rest api", "aws", "graphql", "redis", "ci/cd"],
        "description": "Architects responsive, high-performance client applications and distributed server-side microservices."
    },
    "Cloud & DevOps Architect": {
        "required_skills": ["aws", "docker", "kubernetes", "linux", "ci/cd", "git", "python"],
        "bonus_skills": ["azure", "gcp", "sql", "rest api", "redis", "postgresql", "go"],
        "description": "Orchestrates multi-cloud infrastructure, automated GitOps deployment pipelines, and zero-downtime reliability."
    },
    "Data Scientist / Analytics Lead": {
        "required_skills": ["python", "sql", "pandas", "numpy", "machine learning", "data science"],
        "bonus_skills": ["r", "tableau", "power bi", "excel", "scikit-learn", "postgresql", "deep learning"],
        "description": "Extracts actionable enterprise intelligence, develops predictive statistical models, and builds data pipelines."
    },
    "Backend Systems Engineer": {
        "required_skills": ["python", "java", "sql", "postgresql", "rest api", "docker", "git"],
        "bonus_skills": ["redis", "mongodb", "c++", "go", "aws", "linux", "ci/cd", "kubernetes"],
        "description": "Specializes in scalable API engineering, transactional ACID consistency, and distributed database optimization."
    }
}


def calculate_ats_score(text, name, email, phone, skills, links, experience):
    """
    Computes a comprehensive, multi-pillar ATS score and generates
    detailed diagnostic feedback, role matching, strengths, and recommendations.
    """
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)

    # 1. Contact & Header Scoring (Max: 15 pts)
    contact_score = 0
    contact_feedback = []
    
    if name and name != "Not found" and len(name.split()) >= 2:
        contact_score += 4
        contact_feedback.append("Candidate name cleanly formatted")
    else:
        contact_feedback.append("Missing or unclear candidate name in header")

    if email and email != "Not documented":
        contact_score += 4
        contact_feedback.append("Valid professional email detected")
    else:
        contact_feedback.append("No professional email detected")

    if phone and phone != "Not documented":
        contact_score += 4
        contact_feedback.append("Standard direct telephone number detected")
    else:
        contact_feedback.append("Telephone contact number missing")

    if links and len(links) > 0:
        contact_score += 3
        contact_feedback.append(f"Public professional profile verified ({links[0].get('platform', 'Portfolio')})")
    else:
        contact_feedback.append("No LinkedIn or GitHub profile link found")

    contact_score = min(15, contact_score)

    # 2. Section Architecture & Structure (Max: 25 pts)
    section_score = 0
    detected_sections = []
    missing_sections = []

    for section_name, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, text_lower):
            detected_sections.append(section_name)
            section_score += 4.5
        else:
            missing_sections.append(section_name)

    # Word count evaluation (Ideal: 350 - 1000 words for standard 1-2 page resumes)
    word_score = 0
    if 350 <= word_count <= 950:
        word_score = 5
    elif 200 <= word_count < 350 or 950 < word_count <= 1300:
        word_score = 3.5
    elif word_count > 0:
        word_score = 2

    section_score = min(25, round(section_score + word_score, 1))

    # 3. Technical Keyword Breadth & Density (Max: 25 pts)
    skills_score = 0
    num_skills = len(skills) if skills else 0
    
    if num_skills >= 12:
        skills_score = 25
    elif num_skills >= 8:
        skills_score = 21
    elif num_skills >= 5:
        skills_score = 17
    elif num_skills >= 3:
        skills_score = 13
    elif num_skills >= 1:
        skills_score = 8
    else:
        skills_score = 4

    # 4. Action Verbs & Quantifiable Impact (Max: 20 pts)
    detected_verbs = []
    for verb in ACTION_VERBS:
        if re.search(rf"\b{verb}\b", text_lower):
            detected_verbs.append(verb)

    # Detect quantifiable impact patterns (e.g. 40%, $1.2M, 500k, 10x, 25+ users, etc.)
    metric_matches = re.findall(
        r"(?:\d+(?:\.\d+)?%|\$\s*\d+(?:,\d+)*(?:\.\d+)?(?:\s*[kKmMbB])?|\b\d+\s*(?:\+|x|X)\b|\b\d+\s*(?:ms|seconds|minutes|hours|days|engineers|users|clients|requests|transactions|million|billion|thousand)\b)",
        text
    )

    impact_score = 0
    # Verbs score (max 10)
    verb_count = len(detected_verbs)
    if verb_count >= 8:
        impact_score += 10
    elif verb_count >= 5:
        impact_score += 8
    elif verb_count >= 2:
        impact_score += 5
    elif verb_count >= 1:
        impact_score += 3

    # Metrics score (max 10)
    metrics_count = len(metric_matches)
    if metrics_count >= 5:
        impact_score += 10
    elif metrics_count >= 3:
        impact_score += 8
    elif metrics_count >= 1:
        impact_score += 5
    else:
        impact_score += 2

    impact_score = min(20, impact_score)

    # 5. Format, Readability & Parsing Confidence (Max: 15 pts)
    formatting_score = 15
    if word_count < 150:
        formatting_score -= 4
    if "\x00" in text or len(re.findall(r"[^\x00-\x7F]", text)) > (len(text) * 0.15):
        formatting_score -= 3
    if not email:
        formatting_score -= 2
    formatting_score = max(5, formatting_score)

    # Total Overall ATS Score (0 - 100)
    total_ats = round(contact_score + section_score + skills_score + impact_score + formatting_score)
    total_ats = min(99, max(38, total_ats))

    # Grade & Rating Label
    if total_ats >= 88:
        grade = "A+"
        rating = "ATS Ready (Top 5%)"
        rating_color = "emerald"
    elif total_ats >= 78:
        grade = "A"
        rating = "Highly Competitive Fit"
        rating_color = "emerald"
    elif total_ats >= 68:
        grade = "B+"
        rating = "Qualified (Minor Revisions Recommended)"
        rating_color = "blue"
    elif total_ats >= 55:
        grade = "B"
        rating = "Moderate Alignment"
        rating_color = "amber"
    else:
        grade = "C"
        rating = "Structural Revisions Required"
        rating_color = "rose"

    # Actionable Enterprise Checklist items
    checklist = [
        {
            "category": "Contact Verification",
            "title": "Candidate Identity & Direct Coordinates",
            "passed": bool(email and email != "Not documented" and phone and phone != "Not documented"),
            "detail": "Standard email and direct telephone formatting validated for automated ingestion." if (email and phone) else "Ensure direct telephone and professional email are clearly listed in the header.",
            "impact": "High"
        },
        {
            "category": "Digital Profiles",
            "title": "Digital Professional Portfolio & Links",
            "passed": bool(links and len(links) > 0),
            "detail": f"Active professional repository or network verified: {links[0].get('platform', '')}." if links else "Add a clean, unshortened LinkedIn or GitHub profile link to satisfy recruiter screening standards.",
            "impact": "Medium"
        },
        {
            "category": "Standard Sections",
            "title": "Standard ATS Document Hierarchy",
            "passed": len(detected_sections) >= 4,
            "detail": f"{len(detected_sections)} of 6 standard section headers detected." + (f" Missing: {', '.join(missing_sections[:2])}." if missing_sections else " Complete structural alignment."),
            "impact": "High"
        },
        {
            "category": "Technical Breadth",
            "title": "Technical Competency Inventory",
            "passed": num_skills >= 6,
            "detail": f"{num_skills} technical competencies successfully extracted across domain taxonomy." if num_skills >= 6 else "Expand the technical skills inventory to include 6+ targeted domain keywords.",
            "impact": "High"
        },
        {
            "category": "Quantifiable Proof",
            "title": "Measurable Impact & KPI Metrics",
            "passed": metrics_count >= 2,
            "detail": f"Detected {metrics_count} quantifiable data points demonstrating measurable business impact." if metrics_count >= 2 else "Incorporate quantifiable performance indicators (%, scale metrics, cost efficiency) into recent role bullet points.",
            "impact": "Critical"
        },
        {
            "category": "Action Language",
            "title": "Action-Oriented Leadership Verbs",
            "passed": verb_count >= 4,
            "detail": f"Identified {verb_count} high-impact leadership verbs (e.g., {', '.join(detected_verbs[:3])})." if verb_count >= 4 else "Begin bullet points with proactive verbs such as 'Architected', 'Spearheaded', 'Optimized'.",
            "impact": "Medium"
        }
    ]

    # Strengths summary (Professional phrasing)
    strengths = []
    if num_skills >= 8:
        strengths.append(f"Extensive technical keyword inventory ({num_skills} recognized competencies mapped across industry frameworks).")
    if contact_score >= 12:
        strengths.append("Deterministic contact coordinates and candidate identity header structured for zero ATS parser drop-off.")
    if metrics_count >= 3:
        strengths.append(f"Consistent emphasis on measurable business impact ({metrics_count} quantifiable performance metrics identified).")
    if verb_count >= 5:
        strengths.append(f"Proactive executive vocabulary utilizing {verb_count} high-impact leadership action verbs.")
    if "Work Experience / History" in detected_sections and "Education & Academics" in detected_sections:
        strengths.append("Standard chronological hierarchy aligned with enterprise ATS ingestion guidelines.")
    if not strengths:
        strengths.append("Clear document stream legibility with clean vector extraction.")

    # Tailored Improvements (Professional phrasing)
    improvements = []
    if metrics_count < 3:
        improvements.append("Incorporate more quantifiable performance metrics (latency reduction %, throughput scale, cost savings) into recent role descriptions.")
    if num_skills < 8:
        improvements.append("Enrich the Technical Skills inventory with high-demand domain proficiencies (Cloud, Containers, Databases, CI/CD).")
    if not links:
        improvements.append("Add a direct, clean hyperlink to your LinkedIn or GitHub profile in the document header block.")
    if missing_sections:
        improvements.append(f"Maintain standard section headers for: {', '.join(missing_sections[:2])} to prevent ATS parser truncation.")
    if verb_count < 4:
        improvements.append("Replace passive descriptions ('Responsible for...', 'Worked on...') with active verbs ('Architected', 'Engineered', 'Orchestrated').")
    if not improvements:
        improvements.append("Maintain keyword currency by aligning specific frameworks with target job postings.")

    # Target Job Role Matching Breakdown
    skills_lower_set = set(s.lower() for s in skills)
    role_matching = {}

    for role_name, role_data in JOB_PROFILES.items():
        req = role_data["required_skills"]
        bonus = role_data["bonus_skills"]
        
        matched_req = [s for s in req if s in skills_lower_set]
        missing_req = [s for s in req if s not in skills_lower_set]
        matched_bonus = [s for s in bonus if s in skills_lower_set]
        missing_bonus = [s for s in bonus if s not in skills_lower_set]

        # Calculate exact required skills match percentage
        req_match_pct = round((len(matched_req) / len(req)) * 100)
        overall_match = min(98, max(25, round(req_match_pct * 0.8 + (len(matched_bonus) / max(1, len(bonus))) * 20)))

        all_required_breakdown = [
            {
                "skill": s.upper(),
                "status": "matched" if s in skills_lower_set else "missing"
            }
            for s in req
        ]

        # Generate screening questions dynamically for this exact role based strictly on resume skills
        role_screening_questions = generate_role_screening_questions(skills, role_name, name, text)

        role_matching[role_name] = {
            "match_percentage": overall_match,
            "required_match_percentage": req_match_pct,
            "total_required_count": len(req),
            "matched_required_count": len(matched_req),
            "description": role_data["description"],
            "all_required_skills": all_required_breakdown,
            "required_skills_list": [s.upper() for s in req],
            "matched_skills": [s.upper() for s in matched_req],
            "missing_skills": [s.upper() for s in missing_req],
            "matched_bonus_skills": [s.upper() for s in matched_bonus],
            "missing_bonus_skills": [s.upper() for s in missing_bonus],
            "status": "Strong Match" if req_match_pct >= 70 else ("Qualified Alignment" if req_match_pct >= 45 else "Development Opportunity"),
            "screening_questions": role_screening_questions
        }

    # Best-matched Role
    best_role = max(role_matching.items(), key=lambda x: x[1]["match_percentage"])

    return {
        "overall_score": total_ats,
        "grade": grade,
        "rating": rating,
        "rating_color": rating_color,
        "breakdown": {
            "contact_header": {
                "score": contact_score,
                "max": 15,
                "percentage": round((contact_score / 15) * 100),
                "label": "Contact & Identifiers"
            },
            "section_structure": {
                "score": section_score,
                "max": 25,
                "percentage": round((section_score / 25) * 100),
                "label": "Section Architecture"
            },
            "keyword_breadth": {
                "score": skills_score,
                "max": 25,
                "percentage": round((skills_score / 25) * 100),
                "label": "Keyword Competencies"
            },
            "impact_metrics": {
                "score": impact_score,
                "max": 20,
                "percentage": round((impact_score / 20) * 100),
                "label": "Quantifiable Impact & Verbs"
            },
            "format_readability": {
                "score": formatting_score,
                "max": 15,
                "percentage": round((formatting_score / 15) * 100),
                "label": "ATS Parsing Readability"
            }
        },
        "stats": {
            "verbs_count": verb_count,
            "metrics_count": metrics_count,
            "detected_sections_count": len(detected_sections),
            "missing_sections_count": len(missing_sections)
        },
        "detected_verbs": [v.capitalize() for v in detected_verbs[:10]],
        "detected_sections": detected_sections,
        "missing_sections": missing_sections,
        "checklist": checklist,
        "strengths": strengths[:4],
        "improvements": improvements[:4],
        "role_matching": role_matching,
        "target_role_recommendation": {
            "role": best_role[0],
            "fit": f"{best_role[1]['match_percentage']}%",
            "required_fit": f"{best_role[1]['required_match_percentage']}%",
            "status": best_role[1]["status"]
        },
        "interview_prep": best_role[1]["screening_questions"]
    }


# Detailed technical question repository keyed by (role, skill)
SKILL_ROLE_QUESTIONS = {
    # --- AI / Machine Learning Engineer ---
    ("AI / Machine Learning Engineer", "deep learning"): {
        "question": "Your resume verifies deep learning experience. How do you address vanishing/exploding gradients in deep networks, choose between AdamW and SGD with cosine annealing, and evaluate loss plateaus during distributed multi-epoch training?",
        "role_demand": "Core Deep Architecture & Training Dynamics Standard",
        "recruiter_intent": "Evaluates foundational deep learning training intuition, loss optimization, and debugging convergence failures.",
        "talking_points": "Address residual connections, gradient clipping, learning rate warmup/decay schedules, and weight decay vs L2 regularization."
    },
    ("AI / Machine Learning Engineer", "pytorch"): {
        "question": "Your resume verifies production experience with PyTorch. For an AI / Machine Learning Engineer role, how do you handle gradient accumulation, mixed-precision (torch.cuda.amp) training, and memory management across multi-GPU distributed clusters (DistributedDataParallel)?",
        "role_demand": "Mandatory Deep Learning Training & Inference Vector",
        "recruiter_intent": "Validates actual hands-on engineering depth with PyTorch beyond high-level tutorial API usage.",
        "talking_points": "Address torch.cuda.amp.autocast, gradient checkpointing to prevent OOM errors, DistributedDataParallel vs DataParallel, and NCCL backend tuning."
    },
    ("AI / Machine Learning Engineer", "tensorflow"): {
        "question": "Your resume lists TensorFlow. In production AI inference, how do you optimize model computation graphs using TensorRT, TF Serving, and quantization-aware training to minimize P99 latency under heavy concurrent request spikes?",
        "role_demand": "Production Neural Graph & Model Serving Requirement",
        "recruiter_intent": "Evaluates capability to deploy high-throughput, low-latency models to production serving infrastructure.",
        "talking_points": "Explain SavedModel optimization, dynamic batching in TF Serving, INT8 post-training quantization, and XLA compilation."
    },
    ("AI / Machine Learning Engineer", "nlp"): {
        "question": "Your resume documents core expertise in NLP. In this AI / ML position, how have you architected and evaluated tokenization pipelines, context window limits, and parameter-efficient fine-tuning (LoRA / QLoRA) for enterprise language models?",
        "role_demand": "Core LLM & Natural Language Architecture Requirement",
        "recruiter_intent": "Probes depth in modern transformer architectures, parameter-efficient tuning, and inference optimization.",
        "talking_points": "Detail LoRA rank sizing, gradient accumulation, Hugging Face Tokenizer caching, attention masking, and RAG retrieval latency reduction."
    },
    ("AI / Machine Learning Engineer", "computer vision"): {
        "question": "Your resume highlights Computer Vision competencies. In real-time video or spatial inference streams, how do you manage input tensor pre-processing pipelines, frame batching, and CUDA stream concurrency to avoid I/O bottlenecks?",
        "role_demand": "Perception & Spatial Tensor Pipeline Standard",
        "recruiter_intent": "Assesses end-to-end hardware-accelerated video/image streaming and edge inference knowledge.",
        "talking_points": "Mention NVIDIA DALI / OpenCV CUDA processing, TensorRT FP16 pipelines, NMS (Non-Maximum Suppression) optimization, and mAP metrics."
    },
    ("AI / Machine Learning Engineer", "python"): {
        "question": "Your resume establishes Python as a foundational language. In high-throughput AI pipelines, how do you navigate GIL (Global Interpreter Lock) constraints and memory leaks during concurrent multi-process tensor loading and model worker execution?",
        "role_demand": "Primary Execution Language & Memory Management",
        "recruiter_intent": "Tests understanding of Python internals, shared memory architectures, and concurrency in ML workflows.",
        "talking_points": "Explain multiprocessing vs multithreading, torch.multiprocessing shared memory arrays, avoiding reference cycles, and C-extension bindings."
    },
    ("AI / Machine Learning Engineer", "docker"): {
        "question": "You list Docker in your technical competencies. For this AI / Machine Learning Engineer position, how do you construct multi-stage Dockerfiles with NVIDIA CUDA base images to reduce final image footprint from 15GB+ down to lean production artifacts?",
        "role_demand": "Containerized ML Runtime & GPU Packaging Standard",
        "recruiter_intent": "Verifies ability to build lean, secure, and reproducible GPU container environments for cluster orchestration.",
        "talking_points": "Discuss multi-stage build caching, nvidia-container-toolkit runtime flags, stripping build-time wheels, and minimal base layers (distroless/alpine)."
    },
    ("AI / Machine Learning Engineer", "git"): {
        "question": "Your resume verifies Git version control. In distributed machine learning development, how do you version large model checkpoint binaries, experiment hyperparameter manifests, and dataset lineage alongside codebase commits?",
        "role_demand": "MLOps Experiment Tracking & Reproducibility Standard",
        "recruiter_intent": "Evaluates discipline in production experiment reproducibility, data lineage, and collaborative model tracking.",
        "talking_points": "Discuss Git LFS pointers, DVC (Data Version Control) remotes, MLflow run artifacts, and automated CI/CD model validation triggers."
    },
    ("AI / Machine Learning Engineer", "machine learning"): {
        "question": "Based on your verified Machine Learning background in your resume, walk through how you detect dataset drift, feature covariate shift, and concept drift in production feature stores post-deployment.",
        "role_demand": "Model Governance, Drift Detection & Production Monitoring",
        "recruiter_intent": "Ensures the candidate understands the full model lifecycle beyond initial offline train/test splits.",
        "talking_points": "Explain Kolmogorov-Smirnov statistical testing, Population Stability Index (PSI), Prometheus metrics instrumentation, and automated shadow evaluation."
    },

    # --- Full Stack Software Engineer ---
    ("Full Stack Software Engineer", "javascript"): {
        "question": "Your resume highlights JavaScript / TypeScript. For this Full Stack role, how do you architect shared type definitions between the frontend client and backend APIs to prevent runtime serialization regressions?",
        "role_demand": "Full Stack Type Safety & Client-Server Contract",
        "recruiter_intent": "Verifies end-to-end type safety, API schema validation, and defensive programming across tiers.",
        "talking_points": "Discuss Zod schema parsing, OpenAPI / GraphQL codegen, tRPC, and handling asynchronous boundary exceptions."
    },
    ("Full Stack Software Engineer", "typescript"): {
        "question": "Your resume indicates TypeScript proficiency. How do you leverage advanced utility types, generics, and strict compiler configurations to eliminate 'any' leaks across large full-stack component codebases?",
        "role_demand": "Strict Typing & Enterprise Code Quality Requirement",
        "recruiter_intent": "Probes depth of TypeScript compiler capabilities, interface segregation, and static code verification.",
        "talking_points": "Explain Conditional types, Mapped types, unknown vs any, discriminated unions, and tsconfig strict compiler flags."
    },
    ("Full Stack Software Engineer", "react"): {
        "question": "Your resume documents React development experience. In a complex enterprise application, how do you isolate component re-renders, optimize reconciliation, and manage server cache synchronization vs ephemeral UI state?",
        "role_demand": "Client-Side Rendering Architecture & State Standard",
        "recruiter_intent": "Assesses performance profiling skills and state management architecture in modern frontend apps.",
        "talking_points": "Explain React Server Components, TanStack Query cache invalidation, useMemo/useCallback profiler analysis, and bundle code-splitting."
    },
    ("Full Stack Software Engineer", "node.js"): {
        "question": "You list Node.js in your resume competencies. How do you diagnose event-loop lag under high concurrent throughput, and how do you handle stream backpressure when piping large file payloads or database cursors to HTTP responses?",
        "role_demand": "Asynchronous Server Runtime & Concurrency Requirement",
        "recruiter_intent": "Ensures candidate understands single-threaded asynchronous runtime constraints and non-blocking I/O.",
        "talking_points": "Discuss libuv thread pool sizing, Node clinic.js flame graphs, stream.pipeline with backpressure, and worker threads for CPU tasks."
    },
    ("Full Stack Software Engineer", "python"): {
        "question": "Your resume validates Python proficiency. In a full-stack context, how do you architect asynchronous ASGI backends (FastAPI/Starlette) with connection pooling and background task queues (Celery/RQ) to serve low-latency UI clients?",
        "role_demand": "Full-Stack Server Backend & Concurrency Standard",
        "recruiter_intent": "Evaluates full-stack capability to link responsive frontend state to async backend microservices.",
        "talking_points": "Discuss async/await event loops, async SQLAlchemy session pooling, Redis-backed Celery workers, and WebSocket updates."
    },
    ("Full Stack Software Engineer", "sql"): {
        "question": "Your resume verifies SQL proficiency. For an enterprise Full Stack role, how do you identify and eliminate N+1 query antipatterns generated by ORMs, and how do you structure composite database indexes for filtered pagination?",
        "role_demand": "Database Persistence & Query Efficiency Requirement",
        "recruiter_intent": "Verifies that the full-stack developer understands relational database efficiency rather than blindly relying on ORMs.",
        "talking_points": "Explain EXPLAIN ANALYZE execution cost, eager loading (JOINs / select_related), keyset/cursor-based pagination, and connection pooling."
    },
    ("Full Stack Software Engineer", "git"): {
        "question": "Your resume verifies Git competency. In a fast-moving full-stack team, how do you coordinate monorepo package versioning, automated trunk-based development, and ephemeral preview deployments for pull requests?",
        "role_demand": "Full-Stack CI/CD & Version Control Governance",
        "recruiter_intent": "Tests software engineering release hygiene and multi-package dependency coordination.",
        "talking_points": "Mention Turborepo / Nx caching, atomic commits, GitHub Actions preview environments, and semantic versioning."
    },
    ("Full Stack Software Engineer", "html"): {
        "question": "Your resume documents core web engineering proficiencies. How do you ensure accessible semantic HTML (ARIA roles, WCAG 2.1 compliance) and optimize Core Web Vitals (LCP, INP, CLS) for enterprise web clients?",
        "role_demand": "Accessible Semantic Markup & Web Performance Standard",
        "recruiter_intent": "Probes frontend engineering fundamentals, accessibility standards, and browser rendering pipeline optimization.",
        "talking_points": "Discuss semantic tag hierarchy, aria-live regions, critical CSS inlining, font preloading, and avoiding layout shifts."
    },
    ("Full Stack Software Engineer", "css"): {
        "question": "You document modern styling in your background. How do you approach CSS architecture in large-scale applications—comparing Tailwind CSS, CSS Modules, and CSS-in-JS in terms of bundle weight and runtime performance?",
        "role_demand": "Scalable Style Systems & Browser Painting Performance",
        "recruiter_intent": "Assesses modern UI styling paradigms, design system integration, and zero-runtime-cost CSS choices.",
        "talking_points": "Discuss atomic CSS purging, CSS custom properties for theming, reducing browser recalculate-style overhead, and GPU-accelerated compositing."
    },

    # --- Cloud & DevOps Architect ---
    ("Cloud & DevOps Architect", "aws"): {
        "question": "Your resume documents hands-on AWS experience. For a Cloud & DevOps Architect requisition, walk through how you architect a multi-account, multi-region AWS landing zone with Transit Gateway, private VPC peering, and automated IAM least-privilege boundary enforcement.",
        "role_demand": "Multi-Account Enterprise Cloud Architecture Standard",
        "recruiter_intent": "Probes enterprise cloud networking, security perimeter defense, and Infrastructure-as-Code automation.",
        "talking_points": "Discuss AWS Organizations, Control Tower, Transit Gateway route tables, IAM Permission Boundaries, and Terraform modular state."
    },
    ("Cloud & DevOps Architect", "kubernetes"): {
        "question": "Your resume lists Kubernetes as a core competency. How do you implement Pod Disruption Budgets, Horizontal Pod Autoscalers (HPA) using custom Prometheus metrics, and automated Canary deployment validation using service meshes or ingress controllers?",
        "role_demand": "Cluster Orchestration, Autoscaling & Zero-Downtime Releases",
        "recruiter_intent": "Validates hands-on production cluster administration, traffic shaping, and self-healing workload design.",
        "talking_points": "Explain KEDA / Prometheus Adapter for custom metrics, readiness/liveness probe thresholds, Argo Rollouts, and Istio/Envoy traffic shifting."
    },
    ("Cloud & DevOps Architect", "docker"): {
        "question": "You list Docker in your technical profile. How do you implement container hardening (e.g. non-root users, read-only root filesystems, minimal attack surface via distroless images) and automated vulnerability image scanning (Trivy/Clair) in deployment pipelines?",
        "role_demand": "Container Security & Immutable Artifact Packaging",
        "recruiter_intent": "Assesses security-first containerization practices and supply-chain artifact integrity.",
        "talking_points": "Discuss USER directives, seccomp/AppArmor security profiles, multi-stage compilation, and signing container images with Cosign."
    },
    ("Cloud & DevOps Architect", "ci/cd"): {
        "question": "Your resume validates CI/CD expertise. Describe your architecture for a zero-downtime Blue/Green or Canary release pipeline, including automated rollback triggers on error-budget exhaustion or synthetic canary failure.",
        "role_demand": "Automated Deployment Rigor & Reliability Engineering",
        "recruiter_intent": "Verifies practical implementation of progressive delivery and automated blast-radius containment.",
        "talking_points": "Explain automated smoke testing, Prometheus metric threshold alerts triggering rollback, artifact immutability, and GitOps synchronization."
    },
    ("Cloud & DevOps Architect", "linux"): {
        "question": "Your resume highlights Linux systems expertise. How do you diagnose high CPU iowait, kernel memory fragmentation, and socket exhaustion (TIME_WAIT) under heavy network throughput on production cloud nodes?",
        "role_demand": "Core OS Internals & Systems Diagnostics Standard",
        "recruiter_intent": "Probes low-level operating system observability, kernel tuning, and production outage mitigation.",
        "talking_points": "Discuss sysctl network tuning (tcp_tw_reuse), vm.dirty_ratio, strace/perf diagnostics, and epoll socket limits."
    },
    ("Cloud & DevOps Architect", "git"): {
        "question": "You list Git in your competencies. Describe your GitOps architecture (using ArgoCD or Flux) for continuously reconciling Kubernetes cluster state with declarative Git repositories while preventing configuration drift.",
        "role_demand": "Declarative GitOps Infrastructure Management Standard",
        "recruiter_intent": "Validates understanding of declarative infrastructure, automated reconciliation, and branch protection.",
        "talking_points": "Explain self-healing reconciliation loops, Kustomize overlays for environments, sealed-secrets management, and immutable commit tags."
    },
    ("Cloud & DevOps Architect", "python"): {
        "question": "Your resume includes Python. In Cloud & DevOps automation, how do you utilize Python with the Boto3/Kubernetes SDKs to build custom CLI tooling, automated cloud hygiene scripts, or serverless event handlers?",
        "role_demand": "Cloud Automation Tooling & Systems Scripting Requirement",
        "recruiter_intent": "Evaluates automation mindset and ability to extend cloud infrastructure with robust Python scripts.",
        "talking_points": "Discuss boto3 pagination and exponential backoff retries, AWS Lambda event loop optimization, and mock testing with moto."
    },

    # --- Data Scientist / Analytics Lead ---
    ("Data Scientist / Analytics Lead", "pandas"): {
        "question": "Your resume highlights Pandas and NumPy. When processing datasets that approach or exceed system RAM, what strategies do you employ (such as categorical downcasting, PyArrow engine backends, or lazy-evaluation libraries like Polars) to maintain computational efficiency?",
        "role_demand": "Data Wrangling & High-Performance Memory Management",
        "recruiter_intent": "Tests efficiency in memory utilization and awareness of modern high-performance data processing frameworks.",
        "talking_points": "Discuss float64/int64 downcasting, pyarrow engine integration, memory_profiler, vectorized SIMD operations, and chunked processing."
    },
    ("Data Scientist / Analytics Lead", "numpy"): {
        "question": "You list NumPy in your core competencies. How do you take advantage of strided arrays, broadcasting semantics, and vectorization to eliminate nested Python loops when computing distance matrices or high-dimensional embeddings?",
        "role_demand": "Vectorized Linear Algebra & Numerical Computing Requirement",
        "recruiter_intent": "Validates computational efficiency, array memory contiguous layout, and mathematical operations.",
        "talking_points": "Discuss C-contiguous vs Fortran-contiguous memory, np.einsum for tensor contraction, broadcasting rules, and avoiding unnecessary array allocations."
    },
    ("Data Scientist / Analytics Lead", "machine learning"): {
        "question": "Your resume verifies Machine Learning expertise. How do you design leakage-free cross-validation pipelines when feature engineering involves target encoding or time-series features, and how do you evaluate model performance on severe class imbalance (e.g. 0.1% positive rate)?",
        "role_demand": "Statistical Rigor & Imbalanced Predictive Modeling",
        "recruiter_intent": "Validates solid foundational machine learning methodology and avoiding subtle training contamination.",
        "talking_points": "Explain scikit-learn Pipeline objects, Stratified TimeSeriesSplit, PR-AUC / Cost-Sensitive loss over ROC-AUC, and calibrated probabilities."
    },
    ("Data Scientist / Analytics Lead", "sql"): {
        "question": "You list SQL in your resume competencies. For analytics and business intelligence, how do you utilize window functions, recursive CTEs, and table partitioning to compute rolling user retention cohorts and multi-touch attribution models?",
        "role_demand": "Advanced Analytical Data Modeling & Query Design",
        "recruiter_intent": "Probes advanced SQL proficiency beyond simple aggregations and joins.",
        "talking_points": "Explain ROW_NUMBER(), DENSE_RANK(), LAG/LEAD for sessionization, recursive common table expressions, and partition pruning."
    },
    ("Data Scientist / Analytics Lead", "python"): {
        "question": "Your resume establishes Python as your analytical foundation. How do you maintain reproducibility in end-to-end data science projects across random seeds, deterministic package lockfiles, and pipeline tracking (e.g., MLflow/Weights & Biases)?",
        "role_demand": "Reproducible Data Science & Scientific Computing Standard",
        "recruiter_intent": "Assesses engineering maturity and experimental rigor in production analytical research.",
        "talking_points": "Discuss environment determinism, pinning random seeds across Python/NumPy/PyTorch, logging artifacts and data hashes, and modular code vs messy notebooks."
    },
    ("Data Scientist / Analytics Lead", "data science"): {
        "question": "Your resume highlights Data Science expertise. In business analytics, how do you design randomized A/B tests with proper sample size power calculations, evaluate statistical significance, and adjust for multi-hypothesis testing (Bonferroni/FDR)?",
        "role_demand": "Statistical Experimentation & Scientific Decision Making",
        "recruiter_intent": "Evaluates statistical depth, experimental design rigor, and commercial impact assessment.",
        "talking_points": "Explain Type I vs Type II errors, statistical power (1 - beta), minimum detectable effect (MDE), and variance reduction techniques (CUPED)."
    },

    # --- Backend Systems Engineer ---
    ("Backend Systems Engineer", "postgresql"): {
        "question": "Your resume validates PostgreSQL experience. For high-concurrency backend services, how do you manage transaction isolation levels, row-level locking (SELECT FOR UPDATE), and connection pool exhaustion using PgBouncer under spike loads?",
        "role_demand": "ACID Relational Persistence & Transaction Concurrency",
        "recruiter_intent": "Tests deep transactional database engineering, concurrency control, and connection pooling.",
        "talking_points": "Discuss Read Committed vs Repeatable Read, deadlocks and lock escalation, PgBouncer transaction pooling mode, and vacuuming tuning."
    },
    ("Backend Systems Engineer", "rest api"): {
        "question": "Your resume documents REST API development. How do you architect idempotent endpoints (e.g. payment processing), structure rate-limiting algorithms across distributed nodes, and propagate distributed tracing context (OpenTelemetry / W3C Trace Context)?",
        "role_demand": "API Scalability, Idempotency & Distributed Tracing",
        "recruiter_intent": "Evaluates enterprise API contract design, resilience, and microservice observability.",
        "talking_points": "Discuss Idempotency-Key headers with Redis SETNX, distributed token bucket rate-limiting, and traceparent header propagation."
    },
    ("Backend Systems Engineer", "redis"): {
        "question": "You document Redis in your core stack. How do you implement robust cache-aside patterns while mitigating cache stampede (thundering herd) and cache penetration, and how do you handle distributed locking using Redlock?",
        "role_demand": "In-Memory Systems, Distributed Caching & Synchronization",
        "recruiter_intent": "Assesses cache architecture maturity and distributed concurrency safety.",
        "talking_points": "Explain probabilistic early expiration (XFetch), bloom filters for non-existent keys, Redis Sentinel/Cluster sharding, and TTL jitter."
    },
    ("Backend Systems Engineer", "python"): {
        "question": "Your resume lists Python backend development. How do you design async I/O worker pools (asyncio/uvloop) vs thread pools for I/O-bound microservices, and how do you profile CPU and memory bottlenecks with cProfile or py-spy?",
        "role_demand": "Asynchronous Backend Concurrency & Runtime Profiling",
        "recruiter_intent": "Evaluates core language runtime mechanics, non-blocking asynchronous patterns, and profiling capability.",
        "talking_points": "Explain event loop blocking avoidance, run_in_executor for CPU tasks, flame graphs, and garbage collection tuning."
    },
    ("Backend Systems Engineer", "java"): {
        "question": "Your resume highlights Java proficiency. For high-throughput enterprise backends, how do you tune JVM garbage collection (G1GC / ZGC), manage thread pool saturation in Spring Boot / Netty, and prevent thread contention on shared locks?",
        "role_demand": "High-Throughput Enterprise JVM Architecture Standard",
        "recruiter_intent": "Tests core JVM performance engineering, memory footprint tuning, and thread concurrency control.",
        "talking_points": "Discuss heap sizing and pauses, Virtual Threads (Project Loom), volatile keyword and CAS atomic variables, and Netty event loops."
    },
    ("Backend Systems Engineer", "sql"): {
        "question": "You list SQL in your backend competencies. How do you design partition keys, analyze query execution plans using EXPLAIN ANALYZE, and eliminate sequential table scans across tables with hundreds of millions of rows?",
        "role_demand": "Relational Persistence Optimization & Query Cost Tuning",
        "recruiter_intent": "Verifies that backend engineer understands index selectivity, query cost, and partitioning.",
        "talking_points": "Discuss B-Tree vs Hash/GIN indexes, composite index column ordering, covering indexes, and range/hash partitioning."
    },
    ("Backend Systems Engineer", "docker"): {
        "question": "Your resume includes Docker. In backend systems, how do you configure container resource limits (CPU quotas, memory cgroups), health probes, and graceful SIGTERM shutdown hooks to prevent connection drops during rolling deployments?",
        "role_demand": "Containerized Runtime Isolation & Graceful Lifecycle",
        "recruiter_intent": "Evaluates production container configuration, zero-downtime termination, and resource isolation.",
        "talking_points": "Discuss dumb-init / tini for PID 1 signal forwarding, draining active database connections, readiness vs liveness probes, and CPU throttling."
    },
    ("Backend Systems Engineer", "git"): {
        "question": "Your resume validates Git in your engineering workflow. In distributed microservice architectures, how do you coordinate API version deprecation, schema migrations, and contract testing across independent backend service releases?",
        "role_demand": "Microservice Release Coordination & Distributed Hygiene",
        "recruiter_intent": "Tests multi-service contract testing, backward compatibility, and release deployment safety.",
        "talking_points": "Discuss Pact contract testing, expand/contract database migration patterns, and automated changelog generation."
    }
}


def generate_role_screening_questions(candidate_skills, target_role, cand_name="Candidate", resume_text=""):
    """
    Generates technical screening questions that are 100% required for the specified target role
    and 100% derived from the candidate's actual extracted resume competencies.
    """
    s_set = set(s.lower() for s in candidate_skills)
    role_data = JOB_PROFILES.get(target_role, {})
    req_skills = [s.lower() for s in role_data.get("required_skills", [])]
    bonus_skills = [s.lower() for s in role_data.get("bonus_skills", [])]

    # Find the intersection between candidate's verified resume skills and the role requirements
    matched_req = [s for s in req_skills if s in s_set]
    matched_bonus = [s for s in bonus_skills if s in s_set]
    missing_req = [s for s in req_skills if s not in s_set]

    questions = []

    # Priority 1: Questions testing skills the candidate HAS in their resume that are REQUIRED for this role
    for skill in matched_req:
        key = (target_role, skill)
        if key in SKILL_ROLE_QUESTIONS:
            q_info = SKILL_ROLE_QUESTIONS[key]
            questions.append({
                "type": "Core Requirement Verification",
                "resume_source": f"Validated in Resume: {skill.upper()}",
                "role_demand": f"Mandatory Requirement for {target_role}",
                "question": q_info["question"],
                "recruiter_intent": q_info["recruiter_intent"],
                "tip": q_info["talking_points"]
            })
        if len(questions) >= 3:
            break

    # Priority 2: Questions testing skills the candidate HAS in their resume that are PREFERRED for this role
    if len(questions) < 4:
        for skill in matched_bonus:
            key = (target_role, skill)
            if key in SKILL_ROLE_QUESTIONS:
                q_info = SKILL_ROLE_QUESTIONS[key]
                questions.append({
                    "type": "Preferred Stack Verification",
                    "resume_source": f"Validated in Resume: {skill.upper()}",
                    "role_demand": f"High-Yield Stack for {target_role}",
                    "question": q_info["question"],
                    "recruiter_intent": q_info["recruiter_intent"],
                    "tip": q_info["talking_points"]
                })
            if len(questions) >= 3:
                break

    # Priority 3: If candidate is missing a critical required skill, ask a bridge transition question based on what they DO have
    if missing_req and matched_req and len(questions) < 4:
        top_missing = missing_req[0].upper()
        top_matched = matched_req[0].upper()
        questions.append({
            "type": "Competency Transition & Gap Probe",
            "resume_source": f"Validated in Resume: {top_matched}",
            "role_demand": f"Target Requisition Demands: {top_missing}",
            "question": f"Your resume validates strong proficiency with {top_matched}, whereas this {target_role} role explicitly requires {top_missing}. How have your engineering principles in {top_matched} prepared you to adopt and deploy production solutions using {top_missing}?",
            "recruiter_intent": f"Evaluates learning agility and practical engineering transfer from {top_matched} to {top_missing}.",
            "tip": f"Highlight conceptual parallels between {top_matched} and {top_missing}, discuss self-directed sandbox projects, and emphasize foundational engineering rigor."
        })

    # Priority 4: Always add an Executive System Design & Architecture Question tailored to the role
    questions.append({
        "type": "System Architecture & Engineering Scalability",
        "resume_source": f"Candidate Profile & Technical Stated Skills: {', '.join([s.upper() for s in candidate_skills[:4]])}",
        "role_demand": f"End-to-End System Design Standard for {target_role}",
        "question": f"Walk through the architectural design of a high-throughput, fault-tolerant production system you would build for a {target_role} role. How do you ensure high availability, telemetry observability, and data consistency under high concurrent scale?",
        "recruiter_intent": "Assesses end-to-end distributed system design maturity, failure domain isolation, and production trade-off decision making.",
        "talking_points": "Structure with Requirements, Data Flow, Component Architecture, Bottlenecks/SPOFs, Caching, and Telemetry Monitoring.",
        "tip": "Structure with Requirements, Data Flow, Component Architecture, Bottlenecks/SPOFs, Caching, and Telemetry Monitoring."
    })

    return questions[:4]


def enhance_bullet_point(bullet_text, skills=None):
    """
    Transforms weak or generic resume bullet points into high-impact,
    ATS-friendly bullet points using the Google XYZ formula (Accomplished [X], as measured by [Y], by doing [Z]).
    """
    cleaned = bullet_text.strip().rstrip(".")
    if not cleaned:
        return []

    # Provide 3 distinct enhanced styles: Technical Depth, Leadership Impact, Scale & Efficiency
    suggestions = [
        {
            "style": "Scale & Quantitative Impact",
            "text": f"Spearheaded {cleaned}, reducing operational latency by 35% and accelerating deployment cycles across 500K+ requests.",
            "formula": "Accomplished [X], measured by [35% latency drop], by doing [Z]"
        },
        {
            "style": "Architecture & Engineering Rigor",
            "text": f"Architected and deployed enterprise-grade solutions for {cleaned}, ensuring 99.9% system availability and strict code quality standards.",
            "formula": "Engineered [High-availability system], measured by [99.9% uptime]"
        },
        {
            "style": "Optimization & Cross-Functional Velocity",
            "text": f"Optimized multi-tier workflows for {cleaned}, automating manual pipelines to save 12+ engineering hours weekly.",
            "formula": "Streamlined [Workflow], measured by [12 hrs/week saved]"
        }
    ]
    return suggestions

