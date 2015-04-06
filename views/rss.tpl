<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
   <atom:link href="{{cfg.get('url')}}/blog/rss.xml" rel="self" type="application/rss+xml" />
   <link>{{cfg.get('url')}}/blog/rss.xml</link>
   <title>{{cfg.get('author')}}: Blog</title>
   <description>This is the RSS feed of {{cfg.get('author')}}'s Blog</description>
   <category>blog</category>
   <copyright>{{author}}</copyright>
   <managingEditor>{{author}}</managingEditor>
   <webMaster>{{author}}</webMaster>
   <pubDate>{{date}}</pubDate>
   <lastBuildDate>{{date}}</lastBuildDate>
   <generator>https://github.com/vijinho/beautifully-simple-static-blog</generator>
   <ttl>1440</ttl>
    %for filename, meta in sorted(data.get('blog_posts_meta').items(), reverse=True):
   <item>
        <pubDate>{{meta.get('rfc822date')}}</pubDate>
        <title>{{meta.get('title')}}</title>
        <description>{{meta.get('title')}}: {{meta.get('tags')}}</description>
        <link>{{cfg.get('url')}}/blog/{{filename[0:-3]}}.html</link>
        <guid>{{cfg.get('url')}}/blog/{{filename[0:-3]}}.html</guid>
   </item>
    %end
 </channel>
</rss>
