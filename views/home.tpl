  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="nine columns" style="margin-top: 25%">
          <h1>{{!data.get('body_title')}}</h1>
          <p>
          I'm <b>Vijay Mahrra</b> and this is my personal blog, I work as a
          <a href="http://uk.linkedin.com/in/vmahrra/en">Full-Stack Web Developer</a>
          - (<a href="https://github.com/vijinho/cv">CV</a>) but I've spent much
          of the last year cycling around the world, taking photographs and
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
        <div class="three columns" style="margin-top: 80%">
            <small>
                <h3>Meta</h3>
                <ul>
                    <li><a href="https://github.com/vijinho/beautifully-simple-static-blog">GitHub</a></li>
                    <li><a href="/blog/docs/CREDITS.html">Credits</a></li>
                    <li><a href="/blog/docs/CHANGES.html">Changes</a></li>
                    <li><a href="/blog/docs/TODO.html">TODO</a></li>
                    <li><a href="/blog/docs/ROADMAP.html">Roadmap</a></li>
                </ul>
            </small>
        </div>
    </div>
  </div>
