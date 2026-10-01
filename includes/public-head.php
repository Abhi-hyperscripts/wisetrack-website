<?php
if (!defined('WISETRACK')) {
    http_response_code(403);
    exit;
}

$pageTitle = $pageTitle ?? 'WiseTrack Blog';
$pageDescription = $pageDescription ?? 'Field notes on custom software engineering, databases, and business operating systems.';
$canonical = $canonical ?? 'https://wisetrack.in/blog.html';
$ogType = $ogType ?? 'website';
$extraHead = $extraHead ?? '';
?>
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <script>(function(){try{if(localStorage.getItem("theme")!=="dark"){document.documentElement.classList.add("light");}else{document.documentElement.classList.remove("light");}}catch(e){}})();</script>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-P32QMPCK');</script>
  <meta name="theme-color" content="#0a0a0c"/>
  <link rel="icon" type="image/svg+xml" href="assets/logo/favicon.svg" />
  <link rel="alternate icon" type="image/png" sizes="32x32" href="assets/logo/favicon-32.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="assets/logo/favicon-180.png" />
  <title><?= e($pageTitle) ?></title>
  <meta name="description" content="<?= e($pageDescription) ?>" />
  <link rel="canonical" href="<?= e($canonical) ?>" />
  <meta property="og:type" content="<?= e($ogType) ?>" />
  <meta property="og:site_name" content="Wisetrack Technologies" />
  <meta property="og:title" content="<?= e($pageTitle) ?>" />
  <meta property="og:description" content="<?= e($pageDescription) ?>" />
  <meta property="og:image" content="https://wisetrack.in/assets/og-image.jpg" />
  <meta property="og:image:type" content="image/jpeg" />
  <meta property="og:image:secure_url" content="https://wisetrack.in/assets/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:url" content="<?= e($canonical) ?>" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://wisetrack.in/assets/og-image.jpg" />
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,30..100,0..1;1,9..144,300..900,30..100,0..1&family=Inter+Tight:wght@300..700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <script src="assets/tailwind-config.js?v=20260620h"></script>
  <link href="assets/styles.css?v=20260620h" rel="stylesheet" />
  <script>document.documentElement.classList.add("js")</script>
  <script src="assets/site.js?v=20260620h" defer></script>
  <?= $extraHead ?>
</head>
