<?php

require dirname(__DIR__) . '/includes/bootstrap.php';

if (admin_user()) {
    header('Location: index.php');
    exit;
}

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    csrf_check();
    $username = trim((string) ($_POST['username'] ?? ''));
    $password = (string) ($_POST['password'] ?? '');
    $stmt = db()->prepare('SELECT * FROM admin_users WHERE username = ?');
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    if ($user && password_verify($password, $user['password_hash'])) {
        session_regenerate_id(true);
        $_SESSION['admin_id'] = (int) $user['id'];
        header('Location: index.php');
        exit;
    }
    $error = 'Those credentials did not match.';
}
?>
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <title>Blog admin login — WiseTrack</title>
  <link rel="icon" type="image/svg+xml" href="../assets/logo/favicon.svg" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="../assets/tailwind-config.js?v=20260620h"></script>
  <link href="../assets/styles.css?v=20260620h" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600;700&display=swap" rel="stylesheet" />
</head>
<body class="bg-bg text-text font-sans antialiased min-h-screen grid place-items-center px-6">
  <form method="post" class="w-full max-w-md bg-surface border border-line rounded-2xl p-8">
    <img src="../assets/logo/wt-mark.svg" alt="" class="h-7 w-auto mb-6" />
    <h1 class="font-display text-3xl">Blog admin</h1>
    <p class="mt-2 text-sm text-text-2">Add and publish journal posts. Inactive posts stay off the website.</p>
    <?php if ($error): ?>
      <p class="mt-4 text-sm text-red-300"><?= e($error) ?></p>
    <?php endif; ?>
    <input type="hidden" name="csrf" value="<?= e(csrf_token()) ?>" />
    <label class="block mt-6 text-xs tracking-widest text-muted">USERNAME
      <input name="username" required autocomplete="username" class="mt-2 w-full rounded-xl bg-bg border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <label class="block mt-4 text-xs tracking-widest text-muted">PASSWORD
      <input type="password" name="password" required autocomplete="current-password" class="mt-2 w-full rounded-xl bg-bg border border-white/10 px-4 py-3 text-sm text-text" />
    </label>
    <button class="mt-6 w-full rounded-xl bg-indigo text-white font-semibold py-3" type="submit">Sign in</button>
  </form>
</body>
</html>
