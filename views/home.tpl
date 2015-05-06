  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="twelve columns">
              <h1>{{!data.get('body_title')}}</h1>
              I make <a href="https://github.com/vijinho/">software and
websites</a> - see my <a href="/blog/cv.html">CV/Resumé</a> - and I'm
passionate about <a
href="http://gettyimages.co.uk/search/photographer?family=creative&photographer=Vijay+Mahrra+%2F+EyeEm">photography</a>&nbsp;and;&nbsp;<a
href="/blog/2014-11-09-touring-latin-america.html">cycling</a>, occassionally <a href="http://vimeo.com/vijinho">shooting videos</a> whilst listening to music on <a href="http://www.last.fm/user/vijinho">last.fm</a>, <a href="http://www.mixcloud.com/vijinho/">Mixcloud</a>&nbsp;and;&nbsp; <a href="http://soundcloud.com/vijinho">SoundCloud</a>, Find out more <a href="http://about.me/vijay.mahrra">about.me</a>...  and then kindly buy me <a href="http://www.amazon.co.uk/gp/registry/wishlist/F66L0QK92OJP/ref=cm_wl_huc_view">a gift</a>.
          <h2>Blog</h2>
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
            <br/>
            %last = 0
            %for filename, meta in sorted(data.get('blog_posts_meta').items(), reverse=True):
              %year = int(meta.get('date')[0:4])
              %if year != last:
                <a href="#{{year}}">{{year}}</a>&nbsp;
              %end
            %last = year
            %end
        </div>
    </div>
  </div>
<br/>
