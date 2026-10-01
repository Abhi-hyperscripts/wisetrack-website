<?php

require __DIR__ . '/_auth.php';
$user = require_admin();

$id = isset($_GET['id']) ? (int) $_GET['id'] : 0;
$post = $id > 0 ? blog_find($id) : null;
if ($id > 0 && !$post) {
    http_response_code(404);
    exit('Post not found.');
}

$errors = [];
$values = $post ?: [
    'title' => '',
    'slug' => '',
    'excerpt' => '',
    'content' => '',
    'category' => 'Journal',
    'author' => 'Anand',
    'author_role' => 'WiseTrack',
    'published_at' => date('Y-m-d'),
    'read_minutes' => 5,
    'status' => 'active',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $values['title'] = trim((string) ($_POST['title'] ?? ''));
    $values['slug'] = trim((string) ($_POST['slug'] ?? ''));
    $values['excerpt'] = trim((string) ($_POST['excerpt'] ?? ''));
    $values['content'] = (string) ($_POST['content'] ?? '');
    $values['category'] = trim((string) ($_POST['category'] ?? ''));
    $values['author'] = trim((string) ($_POST['author'] ?? ''));
    $values['author_role'] = trim((string) ($_POST['author_role'] ?? ''));
    $values['published_at'] = trim((string) ($_POST['published_at'] ?? ''));
    $values['read_minutes'] = (int) ($_POST['read_minutes'] ?? 5);
    $values['status'] = ($_POST['status'] ?? '') === 'inactive' ? 'inactive' : 'active';

    if ($values['title'] === '') {
        $errors[] = 'Title is required.';
    }
    if ($values['excerpt'] === '') {
        $errors[] = 'Excerpt is required.';
    }
    $bodyText = trim(str_replace("\xc2\xa0", ' ', html_entity_decode(strip_tags($values['content']), ENT_QUOTES, 'UTF-8')));
    if ($bodyText === '') {
        $errors[] = 'Article body is required.';
    }
    if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $values['published_at'])) {
        $errors[] = 'Publish date must be a real date.';
    }
    if ($values['read_minutes'] < 1 || $values['read_minutes'] > 180) {
        $errors[] = 'Read time should be between 1 and 180 minutes.';
    }

    $slugSource = $values['slug'] !== '' ? $values['slug'] : $values['title'];
    $slug = unique_slug(slugify($slugSource), $post ? (int) $post['id'] : null);

    if (!$errors) {
        $content = normalize_content($values['content']);
        if ($post) {
            $stmt = db()->prepare(
                'UPDATE blog_posts
                 SET title = ?, slug = ?, excerpt = ?, content = ?, category = ?, author = ?, author_role = ?, published_at = ?, read_minutes = ?, status = ?
                 WHERE id = ?'
            );
            $stmt->execute([
                $values['title'],
                $slug,
                $values['excerpt'],
                $content,
                $values['category'] !== '' ? $values['category'] : 'Journal',
                $values['author'] !== '' ? $values['author'] : 'Anand',
                $values['author_role'] !== '' ? $values['author_role'] : 'WiseTrack',
                $values['published_at'],
                $values['read_minutes'],
                $values['status'],
                (int) $post['id'],
            ]);
            flash('Post updated.');
        } else {
            $stmt = db()->prepare(
                'INSERT INTO blog_posts (title, slug, excerpt, content, category, author, author_role, published_at, read_minutes, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            );
            $stmt->execute([
                $values['title'],
                $slug,
                $values['excerpt'],
                $content,
                $values['category'] !== '' ? $values['category'] : 'Journal',
                $values['author'] !== '' ? $values['author'] : 'Anand',
                $values['author_role'] !== '' ? $values['author_role'] : 'WiseTrack',
                $values['published_at'],
                $values['read_minutes'],
                $values['status'],
            ]);
            flash('Post created.');
        }
        header('Location: index.php');
        exit;
    }
}

admin_layout_start($post ? 'Edit post' : 'New post', $user);
?>
  <div class="mb-8">
    <a href="index.php" class="text-xs font-mono text-muted hover:text-text">← ALL POSTS</a>
    <h1 class="font-display text-4xl mt-3"><?= $post ? 'Edit post' : 'New post' ?></h1>
  </div>

  <?php if ($errors): ?>
    <div class="mb-6 rounded-xl border border-red-400/30 bg-red-400/10 px-4 py-3 text-sm">
      <?php foreach ($errors as $error): ?>
        <p><?= e($error) ?></p>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>

  <form method="post" id="post-form" class="grid gap-5 max-w-4xl">
    <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>" />
    <label class="text-xs tracking-widest text-muted">TITLE
      <input name="title" required value="<?= e($values['title']) ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <label class="text-xs tracking-widest text-muted">SLUG
      <input name="slug" value="<?= e($values['slug']) ?>" placeholder="auto-from-title" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <label class="text-xs tracking-widest text-muted">EXCERPT
      <textarea name="excerpt" required rows="3" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text"><?= e($values['excerpt']) ?></textarea>
    </label>
    <div class="grid sm:grid-cols-2 gap-5">
      <label class="text-xs tracking-widest text-muted">CATEGORY
        <input name="category" value="<?= e($values['category']) ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
      </label>
      <label class="text-xs tracking-widest text-muted">AUTHOR
        <input name="author" value="<?= e($values['author']) ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
      </label>
      <label class="text-xs tracking-widest text-muted">AUTHOR ROLE
        <input name="author_role" value="<?= e($values['author_role']) ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
      </label>
      <label class="text-xs tracking-widest text-muted">PUBLISH DATE
        <input type="date" name="published_at" required value="<?= e($values['published_at']) ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
      </label>
      <label class="text-xs tracking-widest text-muted">READ MINUTES
        <input type="number" min="1" max="180" name="read_minutes" value="<?= (int) $values['read_minutes'] ?>" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
      </label>
      <label class="text-xs tracking-widest text-muted">STATUS
        <select name="status" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text">
          <option value="active" <?= $values['status'] === 'active' ? 'selected' : '' ?>>Active</option>
          <option value="inactive" <?= $values['status'] === 'inactive' ? 'selected' : '' ?>>Inactive</option>
        </select>
      </label>
    </div>
    <div>
      <div class="text-xs tracking-widest text-muted mb-2">ARTICLE BODY</div>
      <textarea id="article-body" name="content" rows="16"><?= e($values['content']) ?></textarea>
    </div>
    <p class="text-xs text-muted -mt-3">Use the toolbar for headings, lists, quotes, and links. The code button shows the HTML.</p>
    <div class="flex gap-3">
      <button class="rounded-xl bg-indigo text-white font-semibold px-5 py-3" type="submit"><?= $post ? 'Save changes' : 'Publish post' ?></button>
      <a href="index.php" class="rounded-xl border border-white/10 px-5 py-3 text-sm">Cancel</a>
    </div>
  </form>
  <script src="https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js"></script>
  <script>
    tinymce.init({
      selector: '#article-body',
      height: 520,
      menubar: false,
      branding: false,
      promotion: false,
      skin: 'oxide-dark',
      content_css: 'dark',
      plugins: 'lists link table code autoresize',
      toolbar: 'undo redo | blocks | bold italic underline | bullist numlist | blockquote | link table | removeformat | code',
      toolbar_mode: 'wrap',
      block_formats: 'Paragraph=p; Heading 2=h2; Heading 3=h3',
      valid_elements: '*[*]',
      extended_valid_elements: '*[*]',
      invalid_elements: 'script,iframe,object,embed,form',
      convert_urls: false,
      relative_urls: false,
      entity_encoding: 'raw',
      content_style: 'body { font-family: "Inter Tight", sans-serif; font-size: 16px; line-height: 1.7; } h2, h3 { font-family: Fraunces, serif; font-weight: 400; }',
      setup: function (editor) {
        editor.on('change input undo redo', function () {
          editor.save();
        });
      }
    });
    document.getElementById('post-form').addEventListener('submit', function () {
      if (window.tinymce) {
        tinymce.triggerSave();
      }
    });
  </script>
<?php
admin_layout_end();
