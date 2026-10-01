<?php

require dirname(__DIR__) . '/includes/bootstrap.php';

function admin_layout_start(string $title, array $user): void
{
    ?>
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <title><?= e($title) ?> — WiseTrack Blog</title>
  <link rel="icon" type="image/svg+xml" href="../assets/logo/favicon.svg" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="../assets/tailwind-config.js?v=20260620h"></script>
  <link href="../assets/styles.css?v=20260620h" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter+Tight:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
</head>
<body class="bg-bg text-text font-sans antialiased min-h-screen">
  <header class="border-b border-white/10 bg-surface/40">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between gap-4">
      <a href="index.php" class="flex items-center gap-2.5">
        <img src="../assets/logo/wt-mark.svg" alt="" class="h-6 w-auto" />
        <span class="font-extrabold tracking-tight">Blog admin</span>
      </a>
      <div class="flex items-center gap-4 text-sm text-text-2">
        <a href="../blog.html" class="hover:text-text" target="_blank" rel="noopener">View blog</a>
        <a href="password.php" class="hover:text-text">Password</a>
        <span class="text-muted"><?= e($user['username']) ?></span>
        <a href="logout.php" class="text-indigo hover:underline">Log out</a>
      </div>
    </div>
  </header>
  <main class="max-w-6xl mx-auto px-6 py-10">
    <?php $message = flash(); if ($message): ?>
      <div class="mb-6 rounded-xl border border-mint/30 bg-mint/10 px-4 py-3 text-sm text-text"><?= e($message) ?></div>
    <?php endif; ?>
    <?php
}

function admin_layout_end(): void
{
    echo '</main></body></html>';
}
