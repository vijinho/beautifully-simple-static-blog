  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <div class="container">
    <div class="row">
      <div class="nine columns" style="margin-top: 25%">
          <h1>{{!data.get('body_title')}}</h1>
          {{!data.get('body_content')}}
          &copy;&nbsp;<a href="http://about.me/vijay.mahrra">Vijay Mahrra</a> {{data.get('date')[0:11]}}
          <hr>
          <small><a href="/blog/index.html">home</a></small>
      </div>
        <div class="three columns" style="margin-top: 25%">
            <small>
                <h3>Meta</h3>
                <ul>
                    <li><a href="http://about.me/vijay.mahrra">About Me</a></li>
                    <li><a href="/blog/docs/cv.html">CV/Resumé</a></li>
                    <li><a href="https://github.com/vijinho/beautifully-simple-static-blog">Source Code</a></li>
                </ul>
            </small>
        </div>
    </div>
  </div>
