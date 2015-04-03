  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="nine columns" style="margin-top: 25%">
          <h1>{{!data.get('body_title')}}</h1>
          <p>
          I work mainly as a
          <a href="http://uk.linkedin.com/in/vmahrra/en">Full-Stack Web Developer (Linked-In)</a>
          but I've spent much of the last year cycling around the world, taking photographs and
          catching up with friends and family. Feel free to connect via
          <a href="http://about.me/vijay.mahrra">about.me</a> or drop a mail to
          vijay.mahrra@gmail.com
          </p>
          <hr>
          <div class="scrollbox-all-blogposts">
            %for filename, meta in sorted(data.get('blog_posts_meta').iteritems(), reverse=True):
              <p>
                  <a href="/blog/{{filename[0:-3]}}.html">{{meta.get('title')}}</a></em>
                  <br/>
                  <small>{{meta.get('date')[0:11]}}</small>
              </p>
            %end
          </div>
        </div>
        <div class="three columns" style="margin-top: 25%">
            <small>
                <h3>Meta</h3>
                <ul>
                    <li><a href="/blog/docs/cv.html">CV/Resumé</a></li>
                    <li><a href="https://github.com/vijinho/beautifully-simple-static-blog">Source Code</a></li>
                </ul>
            </small>
        </div>
    </div>
  </div>
