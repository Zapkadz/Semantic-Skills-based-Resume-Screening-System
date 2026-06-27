<?php

return [
    'driver' => 'api',
    'enabled' => true,

    'api_url' => 'http://ai-api:8000/screening',
    'health_url' => 'http://ai-api:8000/health',
    'recommend_jobs_api_url' => 'http://ai-api:8000/recommend-jobs',

    'api_timeout_seconds' => 180,
    'connect_timeout_seconds' => 5,

    'enable_embedding' => true,
    'embedding_model' => 'BAAI/bge-m3',
    'embedding_local_only' => false,
    'hf_hub_offline' => false,

    'taxonomy_path' => '/opt/semantic_skills_resume/data/taxonomy/skills.json',
    'runtime_dir' => '/var/lib/topcv_ai_runtime',
    'debug_api_payload' => false,
    'debug_ui_diagnostics' => false,
];
