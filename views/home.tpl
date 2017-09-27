  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="twelve columns">
              <h1>{{!data.get('body_title')}}</h1>
              I make <a href="https://github.com/vijinho/">software, apps and
websites</a> and I'm
passionate about <a
href="http://gettyimages.co.uk/search/photographer?family=creative&photographer=Vijay+Mahrra+%2F+EyeEm">photography</a>&nbsp;and&nbsp;<a
href="/blog/2014-11-09-touring-latin-america.html">cycling</a>, occassionally
<a href="http://vimeo.com/vijinho">shooting videos</a> whilst listening to <a
href="http://www.mixcloud.com/vijinho/">Mixcloud</a>&nbsp;and&nbsp; <a
href="http://soundcloud.com/vijinho">SoundCloud</a> and if you have an interesting
proposition, project or opportunity you'd like me to be involved in, drop an
email/gchat to <strong><a
href="mailto:vijay@yoyo.org">vijay@yoyo.org</a></strong> or tweet/gab at
<strong>vijinho</strong>. <a href="/blog/cv.html">CV</a>
          <div class="scrollbox-all-blogposts">
            %last = 0
            %for filename, meta in sorted(data.get('blog_posts_meta').items(), reverse=True):
              %year = int(meta.get('date')[0:4])
              %if year != last:
                <h3><a name="{{year}}"></a>{{year}}</h3>
              %end
              <p>
                  <a href="/blog/{{filename[0:-3]}}.html">{{meta.get('title')}}</a>
                  <br/>
                  <small>{{meta.get('date')[0:11]}}</small>
              </p>
            %last = year
            %end
          </div>
            <small>
            %last = 0
            %for filename, meta in sorted(data.get('blog_posts_meta').items(), reverse=True):
              %year = int(meta.get('date')[0:4])
              %if year != last:
                <a href="#{{year}}">{{year}}</a>&nbsp;
              %end
            %last = year
            %end
            </small>
        </div>
    </div>
  </div>
<br/>
