<?php

require __DIR__ . '/_auth.php';
$user = require_admin();
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $current = (string) ($_POST['current'] ?? '');
    $next = (string) ($_POST['next'] ?? '');
    $stmt = db()->prepare('SELECT password_hash FROM admin_users WHERE id = ?');
    $stmt->execute([(int) $user['id']]);
    $row = $stmt->fetch();
    if (!$row || !password_verify($current, $row['password_hash'])) {
        $error = 'Current password is wrong.';
    } elseif (strlen($next) < 8) {
        $error = 'Use at least 8 characters.';
    } else {
        $update = db()->prepare('UPDATE admin_users SET password_hash = ? WHERE id = ?');
        $update->execute([password_hash($next, PASSWORD_DEFAULT), (int) $user['id']]);
        flash('Password updated.');
        header('Location: index.php');
        exit;
    }
}

admin_layout_start('Password', $user);
?>
  <h1 class="font-display text-4xl mb-6">Change password</h1>
  <?php if ($error): ?>
    <p class="mb-4 text-sm text-red-300"><?= e($error) ?></p>
  <?php endif; ?>
  <form method="post" class="grid gap-4 max-w-md">
    <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>" />
    <label class="text-xs tracking-widest text-muted">CURRENT PASSWORD
      <input type="password" name="current" required class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <label class="text-xs tracking-widest text-muted">NEW PASSWORD
      <input type="password" name="next" required minlength="8" class="mt-2 w-full rounded-xl bg-surface border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <button class="rounded-xl bg-indigo text-white font-semibold px-5 py-3 w-fit" type="submit">Update password</button>
  </form>
<?php
admin_layout_end();
