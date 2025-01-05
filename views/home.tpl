  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <div class="container">
    <div class="row">
        <div class="twelve columns">
              <h1>{{!data.get('body_title')}}</h1>
              Welcome to my homepage, I kiss you!
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
