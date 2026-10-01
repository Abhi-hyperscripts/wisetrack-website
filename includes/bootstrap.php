<?php

define('WISETRACK', true);

$config = require __DIR__ . '/config.php';

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_set_cookie_params([
        'httponly' => true,
        'samesite' => 'Lax',
        'path' => '/',
    ]);
    session_start();
}

function e(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }

    global $config;
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ];

    $server = new PDO(
        'mysql:host=' . $config['db_host'] . ';charset=utf8mb4',
        $config['db_user'],
        $config['db_pass'],
        $options
    );
    $server->exec(
        'CREATE DATABASE IF NOT EXISTS `' . str_replace('`', '', $config['db_name']) . '` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
    );

    $pdo = new PDO(
        'mysql:host=' . $config['db_host'] . ';dbname=' . $config['db_name'] . ';charset=utf8mb4',
        $config['db_user'],
        $config['db_pass'],
        $options
    );

    blog_install($pdo);
    return $pdo;
}

function blog_install(PDO $pdo): void
{
    $pdo->exec(
        "CREATE TABLE IF NOT EXISTS blog_posts (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            slug VARCHAR(190) NOT NULL,
            excerpt TEXT NOT NULL,
            content MEDIUMTEXT NOT NULL,
            category VARCHAR(80) NOT NULL DEFAULT 'Journal',
            author VARCHAR(80) NOT NULL DEFAULT 'Anand',
            author_role VARCHAR(160) NOT NULL DEFAULT 'WiseTrack',
            published_at DATE NOT NULL,
            read_minutes SMALLINT UNSIGNED NOT NULL DEFAULT 5,
            status ENUM('active','inactive') NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uq_blog_slug (slug),
            KEY idx_blog_status_date (status, published_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
    );

    $pdo->exec(
        "CREATE TABLE IF NOT EXISTS admin_users (
            id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_admin_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
    );

    $adminCount = (int) $pdo->query('SELECT COUNT(*) FROM admin_users')->fetchColumn();
    if ($adminCount === 0) {
        global $config;
        $stmt = $pdo->prepare('INSERT INTO admin_users (username, password_hash) VALUES (?, ?)');
        $stmt->execute([
            $config['admin_user'],
            password_hash($config['admin_pass'], PASSWORD_DEFAULT),
        ]);
    }

    $postCount = (int) $pdo->query('SELECT COUNT(*) FROM blog_posts')->fetchColumn();
    if ($postCount === 0) {
        blog_seed($pdo);
    }
}

function blog_seed(PDO $pdo): void
{
    $root = dirname(__DIR__);
    $posts = [
        [
            'title' => 'When to build, when to buy.',
            'slug' => 'when-to-build-when-to-buy',
            'excerpt' => "Most teams should buy off-the-shelf and move on. Some should build something custom. Here's our simple decision framework.",
            'category' => 'HyperScripts',
            'author' => 'Anand',
            'author_role' => 'WiseTrack',
            'published_at' => '2026-02-26',
            'read_minutes' => 7,
            'file' => $root . '/post-when-to-build-when-to-buy.html',
        ],
        [
            'title' => 'Why we turn down half our projects.',
            'slug' => 'why-we-turn-down-half',
            'excerpt' => 'A small, selective engineering team delivers 10x quality. Inside our strict five-point vetting filter for inbound software briefs.',
            'category' => 'HyperScripts',
            'author' => 'Anand',
            'author_role' => 'WiseTrack',
            'published_at' => '2026-01-14',
            'read_minutes' => 5,
            'file' => $root . '/post-why-we-turn-down-half.html',
        ],
        [
            'title' => 'The real cost of the wrong stack.',
            'slug' => 'the-real-cost-of-the-wrong-stack',
            'excerpt' => 'Hiring friction, continuous package updates, and testing drag. Why opting for C# .NET Core and Postgres defaults is a solid decision.',
            'category' => 'HyperScripts',
            'author' => 'Karthik',
            'author_role' => 'WiseTrack',
            'published_at' => '2025-12-05',
            'read_minutes' => 8,
            'file' => $root . '/post-real-cost-of-wrong-stack.html',
        ],
        [
            'title' => 'One app vs. seven.',
            'slug' => 'one-app-vs-seven',
            'excerpt' => 'Case study: Replacing Slack, Zoho, Drive, and Jira inside a 200-person Indian manufacturing organization with one Ragenaizer OS.',
            'category' => 'Ragenaizer',
            'author' => 'Sara',
            'author_role' => 'WiseTrack',
            'published_at' => '2025-10-21',
            'read_minutes' => 6,
            'file' => $root . '/post-one-app-vs-seven.html',
        ],
        [
            'title' => "Postgres is enough, until it isn't.",
            'slug' => 'postgres-is-enough',
            'excerpt' => 'Avoid premature clustering architecture. Scale your relational DB with indexing, partition tables, and ClickHouse vectorized search.',
            'category' => 'Engineering',
            'author' => 'Priya',
            'author_role' => 'WiseTrack',
            'published_at' => '2025-09-11',
            'read_minutes' => 9,
            'file' => $root . '/post-postgres-is-enough.html',
        ],
        [
            'title' => 'Two-week demos beat documents.',
            'slug' => 'two-week-demos',
            'excerpt' => 'Why reading flat PDFs fails compared to clickable prototypes. Prototype-first testing makes development cycles faster.',
            'category' => 'Method',
            'author' => 'Anand',
            'author_role' => 'WiseTrack',
            'published_at' => '2025-08-04',
            'read_minutes' => 4,
            'file' => $root . '/post-two-week-demos.html',
        ],
        [
            'title' => 'Custom Software in Noida: The Digital Shift.',
            'slug' => 'custom-software-in-noida-the-digital-shift',
            'excerpt' => 'Indian SMBs are moving from isolated spreadsheets to integrated, audit-logged enterprise operating databases. What this means for your workflow.',
            'category' => 'Engineering',
            'author' => 'Anand',
            'author_role' => 'Lead Software Engineer, Wisetrack',
            'published_at' => '2026-07-06',
            'read_minutes' => 5,
            'file' => $root . '/blog-detail.html',
        ],
    ];

    $stmt = $pdo->prepare(
        'INSERT INTO blog_posts (title, slug, excerpt, content, category, author, author_role, published_at, read_minutes, status)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    );

    foreach ($posts as $post) {
        $content = blog_extract_html($post['file']);
        if ($content === '') {
            $content = '<p>' . e($post['excerpt']) . '</p>';
        }
        $stmt->execute([
            $post['title'],
            $post['slug'],
            $post['excerpt'],
            $content,
            $post['category'],
            $post['author'],
            $post['author_role'],
            $post['published_at'],
            $post['read_minutes'],
            'active',
        ]);
    }
}

function blog_extract_html(string $file): string
{
    if (!is_file($file)) {
        return '';
    }
    $html = file_get_contents($file);
    if ($html === false) {
        return '';
    }

    if (preg_match('/<article class="col-span-12[^"]*"[^>]*>(.*)<\/article>/s', $html, $match)) {
        return trim($match[1]);
    }

    if (preg_match('/<div class="prose text-text-2">(.*?)<\/div>\s*<!-- RELATED/s', $html, $match)) {
        return trim($match[1]);
    }

    return '';
}

function blog_posts(bool $activeOnly = false): array
{
    $sql = 'SELECT * FROM blog_posts';
    if ($activeOnly) {
        $sql .= " WHERE status = 'active'";
    }
    $sql .= ' ORDER BY published_at DESC, id DESC';
    return db()->query($sql)->fetchAll();
}

function blog_find(int $id): ?array
{
    $stmt = db()->prepare('SELECT * FROM blog_posts WHERE id = ?');
    $stmt->execute([$id]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function blog_find_public(string $slug): ?array
{
    $stmt = db()->prepare("SELECT * FROM blog_posts WHERE slug = ? AND status = 'active'");
    $stmt->execute([$slug]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function blog_related(int $id, int $limit = 2): array
{
    $stmt = db()->prepare(
        "SELECT * FROM blog_posts WHERE status = 'active' AND id <> ? ORDER BY published_at DESC, id DESC LIMIT {$limit}"
    );
    $stmt->execute([$id]);
    return $stmt->fetchAll();
}

function blog_date(string $date, string $format = 'd M Y'): string
{
    $ts = strtotime($date);
    return $ts ? date($format, $ts) : $date;
}

function blog_title_html(string $title): string
{
    $pos = strpos($title, ':');
    if ($pos === false) {
        return e($title);
    }
    $lead = trim(substr($title, 0, $pos + 1));
    $rest = trim(substr($title, $pos + 1));
    if ($rest === '') {
        return e($title);
    }
    return e($lead) . ' <span class="font-display italic text-indigo">' . e($rest) . '</span>';
}

function blog_initial(string $name): string
{
    $name = trim($name);
    return $name === '' ? 'W' : strtoupper(substr($name, 0, 1));
}

function slugify(string $value): string
{
    $slug = strtolower(trim($value));
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug) ?? '';
    $slug = trim($slug, '-');
    return $slug !== '' ? $slug : 'post';
}

function unique_slug(string $slug, ?int $ignoreId = null): string
{
    $base = $slug;
    $i = 2;
    while (true) {
        if ($ignoreId === null) {
            $stmt = db()->prepare('SELECT id FROM blog_posts WHERE slug = ?');
            $stmt->execute([$slug]);
        } else {
            $stmt = db()->prepare('SELECT id FROM blog_posts WHERE slug = ? AND id <> ?');
            $stmt->execute([$slug, $ignoreId]);
        }
        if (!$stmt->fetch()) {
            return $slug;
        }
        $slug = $base . '-' . $i;
        $i++;
    }
}

function normalize_content(string $raw): string
{
    $raw = trim($raw);
    if ($raw === '') {
        return '';
    }
    if ($raw === strip_tags($raw)) {
        $blocks = preg_split("/\r\n|\n|\r/", $raw) ?: [];
        $html = '';
        $buffer = [];
        $flush = static function () use (&$buffer, &$html): void {
            $text = trim(implode("\n", $buffer));
            $buffer = [];
            if ($text === '') {
                return;
            }
            $html .= '<p>' . nl2br(e($text), false) . '</p>';
        };
        foreach ($blocks as $line) {
            if (trim($line) === '') {
                $flush();
                continue;
            }
            $buffer[] = $line;
        }
        $flush();
        return $html;
    }

    $raw = preg_replace('#<script\b[^>]*>.*?</script>#is', '', $raw) ?? $raw;
    $raw = preg_replace('#\son\w+\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)#i', '', $raw) ?? $raw;
    $raw = preg_replace('#javascript\s*:#i', '', $raw) ?? $raw;
    return $raw;
}

function csrf_token(): string
{
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(16));
    }
    return $_SESSION['csrf'];
}

function csrf_check(): void
{
    $sent = $_POST['csrf'] ?? '';
    $known = $_SESSION['csrf'] ?? '';
    if (!is_string($sent) || !is_string($known) || $known === '' || !hash_equals($known, $sent)) {
        http_response_code(400);
        exit('Invalid request.');
    }
}

function flash(string $message = null): ?string
{
    if ($message !== null) {
        $_SESSION['flash'] = $message;
        return null;
    }
    $value = $_SESSION['flash'] ?? null;
    unset($_SESSION['flash']);
    return $value;
}

function admin_user(): ?array
{
    if (empty($_SESSION['admin_id'])) {
        return null;
    }
    $stmt = db()->prepare('SELECT id, username FROM admin_users WHERE id = ?');
    $stmt->execute([(int) $_SESSION['admin_id']]);
    $row = $stmt->fetch();
    return $row ?: null;
}

function require_admin(): array
{
    $user = admin_user();
    if (!$user) {
        header('Location: login.php');
        exit;
    }
    return $user;
}
