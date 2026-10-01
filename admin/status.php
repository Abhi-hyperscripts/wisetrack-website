<?php

require __DIR__ . '/_auth.php';
require_admin();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

csrf_check();
$id = (int) ($_POST['id'] ?? 0);
$status = ($_POST['status'] ?? '') === 'inactive' ? 'inactive' : 'active';
$post = blog_find($id);
if (!$post) {
    http_response_code(404);
    exit('Post not found.');
}

$stmt = db()->prepare('UPDATE blog_posts SET status = ? WHERE id = ?');
$stmt->execute([$status, $id]);
flash($status === 'active' ? 'Post is now active.' : 'Post is now inactive and hidden on the website.');
header('Location: index.php');
exit;
