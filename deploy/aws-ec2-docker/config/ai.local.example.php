<?php

return [
    'provider' => 'groq',
    'api_key' => 'YOUR_GROQ_API_KEY',
    'model' => 'llama-3.3-70b-versatile',
    'timeout_seconds' => 28,
    'max_text_chars' => 14000,
    'groq_base_url' => 'https://api.groq.com/openai/v1',

    'openai' => [
        'api_key' => 'YOUR_OPENAI_OR_PROXY_API_KEY',
        'model' => 'gpt-4o',
        'enabled' => true,
    ],
];
