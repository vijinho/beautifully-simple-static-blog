  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <div class="container">
    <div class="row">
      <div class="twelve columns" style="margin-top: 10%">
          <h1>{{!data.get('body_title')}}</h1>
          {{!data.get('body_content')}}
          <hr>
           <div align="right">
            <a href="/blog/index.html">home</a>
          </div>
          <small>
            &copy;&nbsp;<a href="http://about.me/vijay.mahrra">Vijay Mahrra</a>&nbsp;{{data.get('date')[0:11]}}<br/>
          </small>
      </div>
    </div>
  </div>
<br/>
