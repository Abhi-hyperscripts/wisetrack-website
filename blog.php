<?php

require __DIR__ . '/includes/bootstrap.php';

try {
    $posts = blog_posts(true);
} catch (Throwable $e) {
    readfile(__DIR__ . '/blog.html');
    exit;
}

$schemaPosts = [];
foreach ($posts as $post) {
    $schemaPosts[] = [
        '@type' => 'BlogPosting',
        'headline' => $post['title'],
        'url' => 'https://wisetrack.in/blog-detail.php?slug=' . $post['slug'],
    ];
}

$pageTitle = 'WiseTrack Blog — Software Engineering & Operations Insights for SMBs';
$pageDescription = 'Read field notes and essays on software engineering, custom database scaling, agentic AI deployment, and SaaS vs custom builds for growing businesses.';
$canonical = 'https://wisetrack.in/blog.html';
$extraHead = '<script type="application/ld+json">' . json_encode([
    '@context' => 'https://schema.org',
    '@type' => 'Blog',
    'name' => 'WiseTrack Journal',
    'url' => 'https://wisetrack.in/blog.html',
    'publisher' => ['@id' => 'https://wisetrack.in/#organization'],
    'blogPost' => $schemaPosts,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>';

require __DIR__ . '/includes/public-head.php';
require __DIR__ . '/includes/site-top.php';
?>
  <main class="relative pt-[130px]">
    <section class="relative overflow-hidden py-16 md:py-24 animate-rise">
      <div class="absolute inset-0 -z-10 pointer-events-none">
        <div class="aurora animate-drift" style="top:-20%; left:-10%; opacity:.4"></div>
        <div class="absolute inset-0 bp-grid"></div>
        <div class="absolute inset-0 bg-gradient-to-b from-transparent to-bg"></div>
        <div class="absolute inset-0 grain"></div>
      </div>

      <div class="max-w-page mx-auto px-edge text-center flex flex-col items-center">
        <span class="mono text-xs text-indigo tracking-widest uppercase">FIELD NOTES</span>
        <h1 class="font-display font-light text-[clamp(2.4rem,5.5vw,4.8rem)] leading-[0.98] tracking-[-0.03em] text-text mt-4 max-w-4xl">
          Observations on <span class="font-display italic bg-gradient-to-r from-violet via-indigo to-cyan bg-clip-text text-transparent">building software.</span>
        </h1>
        <p class="mt-6 text-base md:text-lg text-text-2/85 leading-relaxed max-w-2xl">
          B2B SaaS engineering, custom database scaling, and product management lessons learned on Noida-based production servers.
        </p>
      </div>
    </section>

    <section class="py-12 relative">
      <div class="max-w-page mx-auto px-edge">
        <?php if (!$posts): ?>
          <p class="text-center text-text-2/80">No articles are published right now.</p>
        <?php else: ?>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <?php foreach ($posts as $post): ?>
          <article class="p-6 bg-surface border border-line rounded-2xl flex flex-col justify-between hover:border-indigo/30 transition-all duration-300">
            <div>
              <span class="mono text-[10px] text-muted"><?= e(blog_date($post['published_at'])) ?></span>
              <h2 class="font-display text-xl text-text font-semibold mt-3 mb-4"><?= e($post['title']) ?></h2>
              <p class="text-xs text-text-2/80 leading-relaxed mb-6">
                <?= e($post['excerpt']) ?>
              </p>
            </div>
            <a href="blog-detail.php?slug=<?= e($post['slug']) ?>" class="text-xs font-mono font-bold text-indigo hover:underline flex items-center gap-1 mt-4">
              READ ESSAY &rarr;
            </a>
          </article>
          <?php endforeach; ?>
        </div>
        <?php endif; ?>
      </div>
    </section>
  </main>
<?php require __DIR__ . '/includes/site-bottom.php'; ?>
