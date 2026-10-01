<?php

require __DIR__ . '/includes/bootstrap.php';

$slug = trim((string) ($_GET['slug'] ?? ''));
$post = $slug !== '' ? blog_find_public($slug) : null;

if (!$post) {
    http_response_code(404);
    $pageTitle = 'Article not found — WiseTrack Journal';
    $pageDescription = 'This article is not available.';
    $canonical = 'https://wisetrack.in/blog.html';
    $topbarDesktop = 'JOURNAL';
    $topbarMobile = 'JOURNAL';
    require __DIR__ . '/includes/public-head.php';
    require __DIR__ . '/includes/site-top.php';
    echo '<main class="relative pt-[130px]"><section class="max-w-3xl mx-auto px-edge py-24 text-center"><h1 class="font-display text-4xl text-text">This article is not available.</h1><p class="mt-4 text-text-2">It may be unpublished or the link is out of date.</p><a href="blog.html" class="inline-block mt-8 text-xs font-mono font-bold text-indigo hover:underline">ALL ARTICLES &rarr;</a></section></main>';
    require __DIR__ . '/includes/site-bottom.php';
    exit;
}

$related = blog_related((int) $post['id']);
$dateLabel = blog_date($post['published_at'], 'd F Y');
$canonical = 'https://wisetrack.in/blog-detail.php?slug=' . rawurlencode($post['slug']);
$pageTitle = $post['title'] . ' — WiseTrack Journal';
$pageDescription = $post['excerpt'];
$ogType = 'article';
$topbarDesktop = 'JOURNAL · ' . $dateLabel . ' · ' . (int) $post['read_minutes'] . ' min read';
$topbarMobile = 'JOURNAL';
$extraHead = '<style>
    .prose p { margin-top: 1.25rem; margin-bottom: 1.25rem; line-height: 1.8; color: rgba(188, 186, 208, 0.9); }
    .prose h2 { font-family: "Fraunces", serif; font-weight: 300; font-size: 1.75rem; margin-top: 2.5rem; margin-bottom: 1rem; color: var(--text); }
    .prose strong { color: var(--text); font-weight: 600; }
    .prose blockquote { border-left: 4px solid var(--indigo); padding-left: 1.25rem; font-style: italic; color: var(--text-2); margin: 2rem 0; }
    .prose ul { list-style-type: disc; padding-left: 1.5rem; margin: 1.25rem 0; }
    .prose li { margin-bottom: 0.5rem; line-height: 1.7; color: rgba(188, 186, 208, 0.9); }
  </style>
  <script type="application/ld+json">' . json_encode([
    '@context' => 'https://schema.org',
    '@type' => 'BlogPosting',
    'headline' => $post['title'],
    'description' => $post['excerpt'],
    'datePublished' => $post['published_at'],
    'author' => ['@type' => 'Person', 'name' => $post['author']],
    'publisher' => ['@type' => 'Organization', 'name' => 'WiseTrack Technologies'],
    'mainEntityOfPage' => $canonical,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>';

require __DIR__ . '/includes/public-head.php';
require __DIR__ . '/includes/site-top.php';
?>
  <main class="relative pt-[130px]">
    <article class="max-w-3xl mx-auto px-edge py-12 md:py-20">
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-4">
          <span class="px-2.5 py-1 rounded bg-indigo/15 text-indigo text-xs font-semibold"><?= e($post['category']) ?></span>
          <span class="mono text-[10px] text-muted"><?= e($dateLabel) ?> · <?= (int) $post['read_minutes'] ?> min read</span>
        </div>

        <h1 class="font-display font-light text-[clamp(2rem,4.5vw,3.5rem)] leading-[1.08] tracking-[-0.02em] text-text">
          <?= blog_title_html($post['title']) ?>
        </h1>

        <div class="mt-6 flex items-center gap-3 border-t border-b border-line py-4">
          <div class="w-10 h-10 rounded-full bg-indigo/20 flex items-center justify-center font-bold text-indigo"><?= e(blog_initial($post['author'])) ?></div>
          <div>
            <div class="text-xs font-bold text-text"><?= e($post['author']) ?></div>
            <div class="text-[10px] text-muted font-mono uppercase"><?= e($post['author_role']) ?></div>
          </div>
        </div>
      </div>

      <div class="prose text-text-2">
        <?= $post['content'] ?>
      </div>

      <?php if ($related): ?>
      <div class="mt-20 border-t border-line pt-12">
        <h3 class="font-display font-light text-2xl text-text mb-6">Read More Field Notes</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <?php foreach ($related as $item): ?>
          <a href="blog-detail.php?slug=<?= e($item['slug']) ?>" class="p-6 bg-surface border border-line rounded-xl hover:border-indigo/30 block transition-all">
            <span class="mono text-[9px] text-muted"><?= e(blog_date($item['published_at'])) ?></span>
            <h4 class="font-bold text-text mt-2"><?= e($item['title']) ?> &rarr;</h4>
          </a>
          <?php endforeach; ?>
        </div>
      </div>
      <?php endif; ?>
    </article>
  </main>
<?php require __DIR__ . '/includes/site-bottom.php'; ?>
