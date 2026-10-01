<?php

require __DIR__ . '/_auth.php';
require_admin();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

csrf_check();
$id = (int) ($_POST['id'] ?? 0);
$post = blog_find($id);
if ($post) {
    $stmt = db()->prepare('DELETE FROM blog_posts WHERE id = ?');
    $stmt->execute([$id]);
    flash('Post deleted.');
}
header('Location: index.php');
exit;
