  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="eight columns" style="margin-top: 15%">
          <h1>{{!data.get('body_title')}}</h1>
          <p>
          I work mainly as a
          <a href="http://uk.linkedin.com/in/vmahrra/en">Full-Stack Web Developer (Linked-In)</a>
          but I've spent much of the last year cycling around the world, taking photographs and
          catching up with friends and family. Feel free to connect via
          <a href="http://about.me/vijay.mahrra">about.me</a> or drop a mail to
          vijay.mahrra@gmail.com
          </p>
            <hr/>
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
            <small>
            %last = 0
            %for filename, meta in sorted(data.get('blog_posts_meta').items(), reverse=True):
              %year = int(meta.get('date')[0:4])
              %if year != last:
                <a href="#{{year}}">{{year}}</a>
              %end
            %last = year
            %end
            </small>
        </div>
        <div class="four columns" style="margin-top: 15%">
            <h3>Hobbies</h3>
            <ul>
                <li><a href="http://eyeem.com/u/vijinho">EyeEm</a></li>
                <li><a href="http://vijinho.tumblr.com/">Tumblr</a></li>
                <li><a href="http://instagram.com/vijinho/">Instagram</a></li>
                <li><a href="http://vimeo.com/vijinho">Vimeo</a></li>
            </ul>
            <h3>Music</h3>
            <ul>
                <li><a href="http://www.last.fm/user/vijinho">Last.fm</a></li>
                <li><a href="http://www.mixcloud.com/vijinho/">Mixcloud</a></li>
                <li><a href="http://soundcloud.com/vijinho">SoundCloud</a></li>
            </ul>
            <h3>Meta</h3>
            <ul>
                <li><a href="http://www.amazon.co.uk/gp/registry/wishlist/F66L0QK92OJP/ref=cm_wl_huc_view">Wishlist</a>                        
                <li><a href="http://about.me/vijay.mahrra">About Me</a></li>
                <li><a href="/blog/cv.html">CV/Resumé</a></li>
                <li><a href="https://github.com/vijinho/beautifully-simple-static-blog">Source Code</a></li>
                <li><a href="/blog/rss.xml">Subscribe (RSS)</a></li>
            </ul>
        </div>
    </div>
  </div>
