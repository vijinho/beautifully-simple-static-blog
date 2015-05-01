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
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
  <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
  <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
  <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">

%if cfg.get('ga_code'):
<!-- Google Analytics -->
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', '{{cfg.get('ga_code')}}', 'auto');
ga('send', 'pageview');
</script>
<!-- End Google Analytics -->
%end


%if cfg.get('keen_project_id') and cfg.get('keen_write_key') and cfg.get('keen_read_key'):
<!-- Keen.IO -->
<script type="text/javascript">
!function(a,b){a("Keen","https://d26b395fwzu5fz.cloudfront.net/3.2.4/keen.min.js",b)}(function(a,b,c){var d,e,f;c["_"+a]={},c[a]=function(b){c["_"+a].clients=c["_"+a].clients||{},c["_"+a].clients[b.projectId]=this,this._config=b},c[a].ready=function(b){c["_"+a].ready=c["_"+a].ready||[],c["_"+a].ready.push(b)},d=["addEvent","setGlobalProperties","trackExternalLink","on"];for(var g=0;g<d.length;g++){var h=d[g],i=function(a){return function(){return this["_"+a]=this["_"+a]||[],this["_"+a].push(arguments),this}};c[a].prototype[h]=i(h)}e=document.createElement("script"),e.async=!0,e.src=b,f=document.getElementsByTagName("script")[0],f.parentNode.insertBefore(e,f)},this);
var client = new Keen({
    projectId: "{{cfg.get('keen_project_id')}}",
    writeKey: "{{cfg.get('keen_write_key')}}",
    readKey: "{{cfg.get('keen_read_key')}}",
    protocol: "auto",
    host: "api.keen.io/3.0",
    requestType: "jsonp"
});
</script>
<!-- End Keen.IO -->
%end

</head>
<body>

