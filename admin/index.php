<?php

require __DIR__ . '/_auth.php';
$user = require_admin();
$posts = blog_posts(false);

admin_layout_start('Posts', $user);
?>
  <div class="flex items-center justify-between gap-4 mb-8">
    <div>
      <h1 class="font-display text-4xl">Posts</h1>
      <p class="mt-2 text-sm text-text-2">Active posts appear on the blog. Inactive posts stay hidden.</p>
    </div>
    <a href="edit.php" class="rounded-xl bg-indigo text-white font-semibold px-4 py-2.5 text-sm">New post</a>
  </div>

  <div class="overflow-x-auto border border-line rounded-2xl">
    <table class="w-full text-sm text-left">
      <thead class="bg-white/[0.03] text-muted text-[11px] tracking-widest">
        <tr>
          <th class="px-4 py-3 font-medium">TITLE</th>
          <th class="px-4 py-3 font-medium">DATE</th>
          <th class="px-4 py-3 font-medium">STATUS</th>
          <th class="px-4 py-3 font-medium">ACTIONS</th>
        </tr>
      </thead>
      <tbody>
        <?php if (!$posts): ?>
          <tr><td colspan="4" class="px-4 py-8 text-text-2">No posts yet.</td></tr>
        <?php endif; ?>
        <?php foreach ($posts as $post): ?>
          <tr class="border-t border-white/5">
            <td class="px-4 py-4">
              <div class="font-semibold text-text"><?= e($post['title']) ?></div>
              <div class="text-xs text-muted mt-1"><?= e($post['slug']) ?></div>
            </td>
            <td class="px-4 py-4 text-text-2 whitespace-nowrap"><?= e(blog_date($post['published_at'])) ?></td>
            <td class="px-4 py-4">
              <form method="post" action="status.php" class="inline">
                <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>" />
                <input type="hidden" name="id" value="<?= (int) $post['id'] ?>" />
                <input type="hidden" name="status" value="<?= $post['status'] === 'active' ? 'inactive' : 'active' ?>" />
                <button type="submit" class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold <?= $post['status'] === 'active' ? 'bg-mint/15 text-mint' : 'bg-white/5 text-muted' ?>">
                  <span class="h-1.5 w-1.5 rounded-full <?= $post['status'] === 'active' ? 'bg-mint' : 'bg-muted' ?>"></span>
                  <?= $post['status'] === 'active' ? 'Active' : 'Inactive' ?>
                </button>
              </form>
            </td>
            <td class="px-4 py-4">
              <div class="flex items-center gap-3">
                <a class="text-indigo hover:underline" href="edit.php?id=<?= (int) $post['id'] ?>">Edit</a>
                <?php if ($post['status'] === 'active'): ?>
                  <a class="text-text-2 hover:text-text" href="../blog-detail.php?slug=<?= e($post['slug']) ?>" target="_blank" rel="noopener">View</a>
                <?php endif; ?>
                <form method="post" action="delete.php" onsubmit="return confirm('Delete this post?');">
                  <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>" />
                  <input type="hidden" name="id" value="<?= (int) $post['id'] ?>" />
                  <button class="text-red-300 hover:underline" type="submit">Delete</button>
                </form>
              </div>
            </td>
          </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>
<?php
admin_layout_end();
