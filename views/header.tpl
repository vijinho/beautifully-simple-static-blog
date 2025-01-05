<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=Edge"/>
  <title>{{!data.get('head_title')}}</title>
  <meta name="description" content="{{!data.get('head_description')}}">
  <meta name="author" content="{{!data.get('head_author')}}">
  <meta name="keywords" content="{{!data.get('head_keywords')}}">
  <link rel="alternate" type="application/rss+xml" href="{{cfg.get('url')}}/blog/rss.xml" title="{{cfg.get('author')}}'s Blog">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no,minimum-scale=1.0,maximum-scale=1.0,minimal-ui">
  <meta name="HandheldFriendly" content="True"/>

  <!-- CSS
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
%if data.get('css'):
{{!data.get('css')}}
%end
  <link rel="stylesheet" media="all" href="/blog/css/style.css">
  <link rel="stylesheet" media="print" href="/blog/css/print.css">

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="icon" type="image/png" href="/img/favicon.png">
  <link rel="shortcut icon" href="/favicon.ico">

</head>
<body>
