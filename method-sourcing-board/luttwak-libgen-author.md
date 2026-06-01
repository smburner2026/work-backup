<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<META HTTP-EQUIV="CACHE-CONTROL" CONTENT="max-age=604800, must-revalidate">
	<meta name="rating" content="general">
	<!--<link href="/rss/index.php" rel="alternate" type="application/rss+xml" title="News" />-->
	<link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon">
	<title>Library Genesis</title>
		
	<!--[if IE 6]>
	<style>
		body {behavior: url("/csshover3.htc");}
		#menu li .drop {background:url("img/drop.gif") no-repeat right 8px; 
	</style>
	<![endif]-->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css">	
	
<link href="/css/font.min.css" rel="stylesheet">	
<style>
nav.navbar .dropdown:hover > .dropdown-menu {
 display: block; 
}
.bd-placeholder-img {
	font-size: 1.125rem;
	text-anchor: middle;
	-webkit-user-select: none;
	-moz-user-select: none;
	-ms-user-select: none;
	user-select: none;
}
@media (min-width: 768px) {
			.bd-placeholder-img-lg {
			font-size: 3.5rem;
		}
	}

.panel-heading .accordion-toggle:after {
    font-family: "Glyphicons Halflings";  
    content: "\e114";    
    float: right;       
    color: grey;         
}
.panel-heading .accordion-toggle.collapsed:after {
    content: "\e080";   
}
.tooltip-inner {
    max-width: 350px;
    width: 350px; 
}
h1 {
	display: block; 
	font-size: 1.8rem; 
	font-weight: bold; 
	font-family: Georgia, "Times New Roman", Times, serif;  color: #A00000; 
}
#tablelibgen td { 
	font-family: "Pt Sans", Tahoma, Helvetica, sans-serif; 
	margin: 0; 
	padding: 0em 3px; 
	font-size: 1rem;
}

#tablelibgen1 td { 
	font-family: "Pt Sans", Tahoma, Helvetica, sans-serif; 
	margin: 0; 
	padding: 0em 3px; 
	font-size: 1rem;
}

.taghide {
    display: none; 
}
.taghide + label ~ div {
    display: none;
}
/* оформляем текст label */
.taghide + label {
    display: inline-block; 
}
/* вид текста label при активном переключателе */

/* когда чекбокс активен показываем блоки с содержанием  */
.taghide:checked + label + div {
    display: block; 
}



/*.navbar {
	background-color: #BBBBBB;
}*/
	</style>

	<link rel="stylesheet" href="/css/dark-mode.css">
	<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<link rel="stylesheet" type="text/css" href="../css/paginator3000.css" />
<script type="text/javascript" src="../js/paginator3000.js"></script><script type='text/javascript' src='//inopportunefable.com/28/4b/51/284b513767b1a27086dec8171527696f.js'></script>




</head>
<body>    
<nav class="navbar navbar-expand-md navbar-dark bg-secondary  mb-1">
  
   <a class="navbar-brand" href="/index.php">
    <img src="/img/logo.png"  height="30" alt="">
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarCollapse">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="/community/app.php/article/news">NEWS <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="/community/">FORUM <span class="sr-only">(current)</span></a>
      </li>
	
      <li class="nav-item dropdown">
<a class="btn btn-secondary dropdown-toggle" href="/community/ucp.php?mode=login" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          LOGIN
        </a>
        <div class="dropdown-menu" aria-labelledby="dropdown01">    
          <a class="dropdown-item" href="/community/ucp.php?mode=register">Register</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          DOWNLOAD
        </a>
        <div class="dropdown-menu" aria-labelledby="dropdown01">      

          <a class="dropdown-item" href="/mirrors.php">Mirrors</a>
          <a class="dropdown-item" href="http://libgenfrialc7tguyjywa36vtrdcplwpxaw43h6o63dmmwhvavo5rqqd.onion/">TOR</a>

	<div class="dropdown-divider"></div>
         <h6 class="dropdown-header">P2P</h6>
          <a class="dropdown-item" href="/torrents/">Torrents</a>
          <a class="dropdown-item" href="https://ipdl.cat/data/torrents.html">Torrents status</a>
          <a class="dropdown-item" href="/nzb/">Usenet (*.nzb)</a>
          <a class="dropdown-item" href="/soft/">Soft</a>
	<!--https://phillm.net/libgen-stats-table.php-->




	<div class="dropdown-divider"></div>
         <h6 class="dropdown-header">DB Dumps</h6>
          <a class="dropdown-item" href="/dirlist.php?dir=dbdumps">Libgen</a>
          <a class="dropdown-item" href="http://libgen.rs/dbdumps/">libgen.rs (gen.lib.rus.ec)</a>

	<!--<div class="dropdown-divider"></div>
 	 <a class="dropdown-item" href="/magz0/">Unsorted magz</a>
 	 <a class="dropdown-item" href="/fict0/">Unsorted fiction</a>

	 <a class="dropdown-item" href="/comics4/">Unsorted comics</a>
        </div>-->

      </li>

      <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="librarian.php" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          UPLOAD
        </a>
        <div class="dropdown-menu" aria-labelledby="dropdown01">  
          <a class="dropdown-item" href="ftp://ftp.libgen.bz/upload/">FTP</a> 
        </div>
      </li>

      <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="/index.php?req=fmode:last&topics1=all" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          LAST
        </a>

        <div class="dropdown-menu" aria-labelledby="dropdown01">
	<a class="dropdown-item" href="/index.php?req=fmode:last&topics1=all"><b>Files</b></a>

          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=l">Libgen</a>
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=a">Scientific Articles</a> 
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=f">Fiction</a> 
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=c">Comics</a> 
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=m">Magazines</a> 
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=s">Standards</a> 
          <a class="dropdown-item" href="/index.php?req=fmode:last&topics%5B%5D=r">Fiction RUS</a>
	<div class="dropdown-divider"></div>
          <a class="dropdown-item" href="/index.php?req=mode:last&curtab=e">Editions</a> 
          <a class="dropdown-item" href="/index.php?req=mode:last&curtab=s">Series</a>
          <a class="dropdown-item" href="/index.php?req=mode:last&curtab=p">Publishers</a> 
        <!--  <a class="dropdown-item" href="/index.php?req=mode:last&curtab=f">Files</a> -->
          <a class="dropdown-item" href="/index.php?req=mode:last&curtab=a">Authors</a> 
          <a class="dropdown-item" href="/index.php?req=mode:last&curtab=w">Works</a>


  
        </div>


      </li>

      <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          OTHERS
        </a>

        <div class="dropdown-menu" aria-labelledby="dropdown01">  
          <a class="dropdown-item" href="json.php">API</a> 
          <a class="dropdown-item" href="rss.php">RSS</a> 
          <a class="dropdown-item" href="top.php">Top 100 users</a> 
          <a class="dropdown-item" href="stat.php">Stats</a>

	<a class="dropdown-item" href="topics.php">Topics</a>

          <a class="dropdown-item" href="batchsearchindex.php">Batch search</a>  
          <a class="dropdown-item" href="biblioservice.php">Bibliographic services</a>
          <a class="dropdown-item" href="https://wiki.mhut.org/software:libgen_desktop">Libgen librarian for desktop</a>


          <a class="dropdown-item" href="/code/">Source (PHP)</a>
          <a class="dropdown-item" href="/soft/">LG soft</a>
          <!--<a class="dropdown-item" href="/import/">Import local files in LG format</a>-->
          <a class="dropdown-item" href="https://z-library.se/fulltext/">Full text search</a>



        </div>
      </li>



     <!-- <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="topics.php" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          Topics
        </a>
      </li>
-->

      <li class="nav-item dropdown">
        <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          LINKS
        </a>

        <div class="dropdown-menu" aria-labelledby="dropdown01">  


          
          <a class="dropdown-item" href="http://sci-hub.ru">Sci-hub</a> 
          <a class="dropdown-item" href="http://magzdb.org">Magzdb.org</a>

          <a class="dropdown-item" href="http://nlr.ru/rlin/Periodika_rus.php">РНБ</a>
          <a class="dropdown-item" href="http://rsl.ru/">РГБ</a>
          <a class="dropdown-item" href="http://loc.gov/">LOC</a>
          <a class="dropdown-item" href="https://comicvine.gamespot.com/">ComicVine</a>
          <a class="dropdown-item" href="http://cyberleninka.ru/">Cyberleninka</a>
          <a class="dropdown-item" href="http://lib.rus.ec/">Lib.rus.ec</a>
          <a class="dropdown-item" href="http://flibusta.net/">Flibusta.net</a>
          <a class="dropdown-item" href="http://goodreads.com/">Goodreads.com</a>
          <a class="dropdown-item" href="http://worldcat.org/">Worldcat.org</a>
          <a class="dropdown-item" href="https://wiki.archiveteam.org/">Archive team</a>
          <a class="dropdown-item" href="https://www.reddit.com/r/libgen/">Reddit</a>
          <a class="dropdown-item" href="http://annas-archive.org/">Anna's Archive</a>
          <a class="dropdown-item" href="https://welib.org/">Welib</a>
          <a class="dropdown-item" href="https://open-slum.org/">The Shadow Library Uptime Monitor</a>

        </div>

      </li>


      <li class="nav-item dropdown">
        <a class="btn btn-secondary" href="index.php?req=mode:req&curtab=e" role="button" id="dropdownMenuLink"  aria-haspopup="true" aria-expanded="false">
          WANTED
        </a>
      </li>

    </ul>
  </div>

  <div class="nav-link">

    <div class="custom-control custom-switch">
      <input type="checkbox" class="custom-control-input" id="darkSwitch">
      <label class="custom-control-label" for="darkSwitch">🌓</label>
    </div>
    <script src="/js/dark-mode-switch.js"></script>
  </div>
   <a class="navbar-brand" href="setlang.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&lang=ru">RU</a>
</nav>
<form class="card p-2 needs-validation" novalidate id="formlibgen" action="index.php" enctype="multipart/form-data" METHOD="GET">
<div class="input-group mb-3" >
	<input autofocus type="text" class="form-control" placeholder="Input value" name="req" aria-label="input text" aria-describedby="button-addon2" value="Luttwak" required>
	<div class="input-group-append">
	<button class="btn btn-outline-secondary"  id="button-addon2" type="submit">&nbsp;&nbsp;&nbsp;&nbsp;&#128269;&nbsp;&nbsp;&nbsp;&nbsp;</button>
	</div>

	<div class="invalid-feedback">Input value</div>
</div>

<div class="container-fluid">
	<div class="row">
		<div class="col-8">	
			<div class="d-block" id="topic">
				<strong>Search in fields:</strong>
				<input type="checkbox"  class="column-input" id="colt" name="columns[]" value="t">
				<label class="column-label" for="coltitle">Title</label>
				<input type="checkbox" checked class="column-input" id="cola" name="columns[]" value="a">
				<label class="column-label" for="colauthor">Author(s)</label>
				<input type="checkbox"  class="column-input" id="cols" name="columns[]" value="s">
				<label class="column-label" for="colseries">Series</label>
				<input type="checkbox"  class="column-input" id="coly" name="columns[]" value="y">
				<label class="column-label" for="colyear">Year</label>
				<input type="checkbox"  class="column-input" id="colp" name="columns[]" value="p">
				<label class="column-label" for="colpublisher">Publisher</label>
				<input type="checkbox"  class="column-input" id="coli" name="columns[]" value="i">
				<label class="column-label" for="colisbn">ISBN</label>
	  		</div>
	
	  		<div class="d-block" id="object">
				<strong>Search in objects:</strong>
				<input type="checkbox" checked class="column-input" id="objf" name="objects[]" value="f">
				<label class="column-label" for="objf">Files</label>
				<input type="checkbox" checked class="column-input" id="obje" name="objects[]" value="e">
				<label class="column-label" for="obje">Editions</label>
				<input type="checkbox"  class="column-input" id="objs" name="objects[]" value="s">
				<label class="column-label" for="objs">Series</label>
				<input type="checkbox" checked class="column-input" id="obja" name="objects[]" value="a">
				<label class="column-label" for="obja">Authors</label>
				<input type="checkbox"  class="column-input" id="objp" name="objects[]" value="p">
				<label class="column-label" for="objp">Publishers</label>
				<input type="checkbox"  class="column-input" id="objw" name="objects[]" value="w">
				<label class="column-label" for="objw">Works</label>
			</div>
			<div class="d-block" id="column">
				<strong>Search in topics :</strong>
				<input type="checkbox" checked class="column-input" id="topl" name="topics[]" value="l" >
				<label class="column-label" for="topl">Libgen</label>
				<input type="checkbox"  class="column-input" id="topc" name="topics[]" value="c" >
				<label class="column-label" for="topc">Comics</label>
				<input type="checkbox"  class="column-input" id="topf" name="topics[]" value="f" >
				<label class="column-label" for="topf">Fiction</label>
				<input type="checkbox"  class="column-input" id="topa" name="topics[]" value="a" >
				<label class="column-label" for="topa">Scientific Articles</label>
				<input type="checkbox"  class="column-input" id="topm" name="topics[]" value="m" >
				<label class="column-label" for="topm">Magazines</label>
				<input type="checkbox"  class="column-input" id="topr" name="topics[]" value="r" >
				<label class="column-label" for="topr">Fiction RUS</label>
				<input type="checkbox"  class="column-input" id="tops" name="topics[]" value="s" >
				<label class="column-label" for="tops">Standards</label>
			</div>
 		</div>
		<div class="col-4">

			<div >
				<strong>Results per page:</strong>

				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="res25" name="res" class="custom-control-input" value="25" checked>
				<label class="custom-control-label" for="res25">25</label>
				</div>
				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="res50" name="res" class="custom-control-input" value="50" >
				<label class="custom-control-label" for="res50">50</label>
				</div>
				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="res100" name="res" class="custom-control-input" value="100" >
				<label class="custom-control-label" for="res100">100</label>

				</div>
 			</div>
			<div class="d-block">
				<table><tr><td>
					<div class="custom-control custom-switch">
						<input type="checkbox" class="custom-control-input" id="covers" name="covers" >
						<label class="custom-control-label" for="covers"><strong>Show Covers</strong></label>
						<script type="text/javascript">
						$("input[id=covers]").change(function(){
							if($(this).is(":checked")==false)
							{
								document.cookie = "covers=; expires=Thu 01-Jan-70 00:00:01 GMT;";
							}
						});				
						</script>
					</div>
					</td><td> 
					<div class="custom-control custom-switch">
						<input type="checkbox" class="custom-control-input" id="showch" name="showch" >
						<label class="custom-control-label" for="showch"><strong>Show chapters</strong></label>
						<script type="text/javascript">
						$("input[id=showch]").change(function(){
							if($(this).is(":checked")==false)
							{
								document.cookie = "showch=; expires=Thu 01-Jan-70 00:00:01 GMT;";
							}
						});				
						</script>
					</div>
				</td></tr></table>

 			</div>

			<div class="d-block">

				<div class="custom-control custom-switch">
					<input type="checkbox" class="custom-control-input" id="gmode" name="gmode" >
					<label class="custom-control-label" for="gmode" ><strong>Google mode <a href="#" data-toggle="modal" data-target="#googlemodemodal">?</a></strong></label>
					<script type="text/javascript">
					$("input[id=gmode]").change(function(){
						if($(this).is(":checked")==false)
						{
							document.cookie = "gmode=; expires=Thu 01-Jan-70 00:00:01 GMT;";
						}
					});
					</script>
					
				</div>
 			</div>

			<div >


				<strong>Seach in files:</strong>

				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="all" name="filesuns" class="custom-control-input" value="all" checked>
				<label class="custom-control-label" for="all">All</label>
				</div>
				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="sort" name="filesuns" class="custom-control-input" value="sort" >
				<label class="custom-control-label" for="sort">Only sorted</label>
				</div>
				<div class="custom-control custom-radio custom-control-inline">
				<input type="radio" id="unsort" name="filesuns" class="custom-control-input" value="unsort" >
				<label class="custom-control-label" for="unsort">Only uns.</label>
				</div>



 			</div>

 		</div>
	</div>
</div>
</form><ul class="nav nav-tabs "><li class="nav-item">
 <a class="nav-link active " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f">Files <span class="badge badge-primary">67</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=e">Editions <span class="badge badge-primary">80</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=s">Series</a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=a">Authors <span class="badge badge-primary">2</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=p">Publishers</a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=w">Works</a>
</li><li class="navbar-right" style="float: right !important;"><a class="nav-link" href="/json.php?object=f&ids=91522068,91599705,92343426,92499298,92606691,92606697,92615939,92615940,92697492,92697493,93133891,93190535,93190536,93487967,93519466,93556857,93637918,93812241,93812247,93812249,93812250,93812253,93812364,93812365,93812366,93812367,93812369,93859924,93865667,94004533,97480081,97480082,97884818,98321831,99728282,100075526,100274039,100285367,101163899,101163913,101221191,101254427,101754149,101754150,102644522,103641599,103657220,103769636,103771747,104006467,104048817,104053390,106081206,106909245,107217676,107933980,108598222,109170210,109260914,110525995,111929831,113058335,114853036,114878196,115094572,115268040,115523956"><font color="black">JSON</font></a></li> </ul><div style="text-align: center;" class="paginator" id="paginator_example_top"></div><script type="text/javascript">paginator_example_top = new Paginator("paginator_example_top", 3, 25, 1, "/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><table class="table  table-striped" id="tablelibgen"><thead><tr>

<th scope="col" class="first_col"><nobr>
ID <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=f_id&ordermode=asc">&#8597</a> 
Time add. <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=time_added&ordermode=asc">&#8597</a> 
Title <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=title&ordermode=asc">&#8597</a> 
Series <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=series&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Author(s) <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=author&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Publisher <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=publisher&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Year <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=year&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Language</th>
<th scope="col">Pages</th>
<th scope="col"><nobr>Size  <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=filesize&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Ext. <a href="/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=extension&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Mirrors</th>
</tr></thead><tbody><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-29; ID: 91522068<br>_210271.684a231814029b3d4b01e08eb5c112ea" href="edition.php?id=136202896">Coup d'Etat: A Practical Handbook <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-29; ID: 91522068<br>_210271.684a231814029b3d4b01e08eb5c112ea" href="edition.php?id=136202896"><i><font color="green"> 0674175476; 9780674175471</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 425629</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td></td>
<td><nobr>1979</nobr></td>
<td>English</td>
<td>234 / 216</td>
<td><nobr><a href="/file.php?id=91522068">13 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=684a231814029b3d4b01e08eb5c112ea"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/684a231814029b3d4b01e08eb5c112ea"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/684a231814029b3d4b01e08eb5c112ea?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/684a231814029b3d4b01e08eb5c112ea"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/684a231814029b3d4b01e08eb5c112ea"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-30; ID: 91599705<br>_211705.ae46bfbac7b502d510cf36db73c706f7" href="edition.php?id=136284127">The Grand Strategy of the Byzantine Empire <i>First Edition</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-30; ID: 91599705<br>_211705.ae46bfbac7b502d510cf36db73c706f7" href="edition.php?id=136284127"><i><font color="green"> 0674035194; 9780674035195</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 506860</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>THE BELKNAP PRESS OF HARVARD UNIVERSITY PRESS</td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>513 / 513</td>
<td><nobr><a href="/file.php?id=91599705">2 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=ae46bfbac7b502d510cf36db73c706f7"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/ae46bfbac7b502d510cf36db73c706f7"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/ae46bfbac7b502d510cf36db73c706f7?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/ae46bfbac7b502d510cf36db73c706f7"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/ae46bfbac7b502d510cf36db73c706f7"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-11-15/2019-12-21; ID: 92343426<br>Luttwak - The Rise of China Vs. The Logic of Strategy" href="edition.php?id=137072320">The Rise of China vs. the Logic of Strategy <i>1st</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-11-15/2019-12-21; ID: 92343426<br>Luttwak - The Rise of China Vs. The Logic of Strategy" href="edition.php?id=137072320"><i><font color="green"> 0674066421; 9780674066427</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1295053</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Belknap Press</td>
<td><nobr>2012</nobr></td>
<td>English</td>
<td>321 / 320</td>
<td><nobr><a href="/file.php?id=92343426">1 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=3b0be7e5f20682e68e3a5342047e23c0"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/3b0be7e5f20682e68e3a5342047e23c0"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/3b0be7e5f20682e68e3a5342047e23c0?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/3b0be7e5f20682e68e3a5342047e23c0"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/3b0be7e5f20682e68e3a5342047e23c0"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-03-14/2021-10-08; ID: 92499298<br>10.1007%2F978-1-349-17410-2" href="edition.php?id=137241153">International Security Yearbook 1983/84 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-03-14/2021-10-08; ID: 92499298<br>10.1007%2F978-1-349-17410-2" href="edition.php?id=137241153"><i><font color="green"> 9780333369302; 0333369300; 9781349174102; 1349174106</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-03-14/2021-10-08; ID: 92499298<br>10.1007%2F978-1-349-17410-2" href="edition.php?id=137241153"><i><font color="green">DOI: 10.1007/978-1-349-17410-2</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1463886</span></nobr>

</td>
<td>Barry M. Blechman, Edward N. Luttwak (eds.)</td>
<td>Palgrave Macmillan</td>
<td><nobr>1984</nobr></td>
<td>English</td>
<td>351</td>
<td><nobr><a href="/file.php?id=92499298">29 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=7931fe82fee0fb648fec6ebf3083125a"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/7931fe82fee0fb648fec6ebf3083125a"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/7931fe82fee0fb648fec6ebf3083125a?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/7931fe82fee0fb648fec6ebf3083125a"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/7931fe82fee0fb648fec6ebf3083125a"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-11-22/2019-12-21; ID: 92606691<br>Edward Luttwak - La grande strategia dell__039;Impero Bizantino" href="edition.php?id=137361997">La grande strategia dell’impero bizantino <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1584730</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>BUR Biblioteca Univ. Rizzoli</td>
<td><nobr>2011</nobr></td>
<td>Italian</td>
<td>381 / 0</td>
<td><nobr><a href="/file.php?id=92606691">3 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d47a8419683ab4cdd8eccb4d25f44cf8"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d47a8419683ab4cdd8eccb4d25f44cf8"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d47a8419683ab4cdd8eccb4d25f44cf8?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d47a8419683ab4cdd8eccb4d25f44cf8"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-11-22/2021-10-02; ID: 92606697<br>Edward Luttwak - Tecnica del colpo di Stato (1969)" href="edition.php?id=137362003">Tecnica del colpo di Stato <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1584736</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Longanesi</td>
<td><nobr>1969</nobr></td>
<td>Italian</td>
<td>271 / 271</td>
<td><nobr><a href="/file.php?id=92606697">7 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=3f1fb9e9d002373bd71798cda171f4eb"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/3f1fb9e9d002373bd71798cda171f4eb"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/3f1fb9e9d002373bd71798cda171f4eb?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/3f1fb9e9d002373bd71798cda171f4eb"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-12-09/2022-03-25; ID: 92615939<br>Luttwak, Edward N. - The Grand Strategy of the Roman Empire" href="edition.php?id=137372456">The Grand Strategy of the Roman Empire: From the First Century A.D. to the Third <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-12-09/2022-03-25; ID: 92615939<br>Luttwak, Edward N. - The Grand Strategy of the Roman Empire" href="edition.php?id=137372456"><i><font color="green"> 0801821584; 9780801821585</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1595189</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Johns Hopkins University Press</td>
<td><nobr>1979</nobr></td>
<td>English</td>
<td>0 / 272</td>
<td><nobr><a href="/file.php?id=92615939">4 MB</a></nobr></td>
<td>azw</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=cf8cfd7fca0d55cdb74f61bc0535ddb9"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/cf8cfd7fca0d55cdb74f61bc0535ddb9"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/cf8cfd7fca0d55cdb74f61bc0535ddb9?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/cf8cfd7fca0d55cdb74f61bc0535ddb9"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-12-09/2021-10-02; ID: 92615940<br>Coup D__039;Etat_ A Practical Handbook, Revised - Edward N. Luttwak" href="edition.php?id=137372458">Coup d’État: A Practical Handbook <i>Revised</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-12-09/2021-10-02; ID: 92615940<br>Coup D__039;Etat_ A Practical Handbook, Revised - Edward N. Luttwak" href="edition.php?id=137372458"><i><font color="green"> 0674737261; 9780674737266</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1595191</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Harvard University Press</td>
<td><nobr>2016</nobr></td>
<td>English</td>
<td>0 / 304</td>
<td><nobr><a href="/file.php?id=92615940">1 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=5e48f2c1e9e7b0f050263377efffea9a"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/5e48f2c1e9e7b0f050263377efffea9a"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/5e48f2c1e9e7b0f050263377efffea9a?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/5e48f2c1e9e7b0f050263377efffea9a"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b>Studies in Air Power<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697492<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460267"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697492<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460267">Strategic Air Power in Desert Storm <i>1</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697492<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460267"><i><font color="green"> 0714651931; 9780714651934</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1683000</span></nobr>

</td>
<td>John Andreas Olsen, Edward N. Luttwak</td>
<td>Routledge</td>
<td><nobr>2003</nobr></td>
<td>English</td>
<td>0 / 256</td>
<td><nobr><a href="/file.php?id=92697492">7 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=080770880039c35795da46561de1bbba"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/080770880039c35795da46561de1bbba"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/080770880039c35795da46561de1bbba?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/080770880039c35795da46561de1bbba"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b>Studies in Air Power<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697493<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460268"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697493<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460268">Strategic Air Power in Desert Storm <i>1</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-05-10/2021-10-03; ID: 92697493<br>Strategic Air Power in Desert Storm 0-7 1 46 - 5 1 9 3 - 1" href="edition.php?id=137460268"><i><font color="green"> 0714651931; 9780714651934</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1683001</span></nobr>

</td>
<td>John Andreas Olsen, Edward N. Luttwak</td>
<td>Routledge</td>
<td><nobr>2003</nobr></td>
<td>English</td>
<td>345 / 256</td>
<td><nobr><a href="/file.php?id=92697493">5 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d6fed78486b9c4bb638e5934609a2444"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d6fed78486b9c4bb638e5934609a2444"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d6fed78486b9c4bb638e5934609a2444?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d6fed78486b9c4bb638e5934609a2444"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-10-12/2019-12-21; ID: 93133891<br>Edward N. Luttwak - Tecnica del colpo di Stato" href="edition.php?id=137902936">Tecnica del colpo di Stato <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2125669</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Longanesi</td>
<td><nobr>1969</nobr></td>
<td>Italian</td>
<td>273 / 273</td>
<td><nobr><a href="/file.php?id=93133891">7 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=0da1d2a0393a33b7ae848d48b9eadeed"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/0da1d2a0393a33b7ae848d48b9eadeed"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/0da1d2a0393a33b7ae848d48b9eadeed?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/0da1d2a0393a33b7ae848d48b9eadeed"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-02-21/2019-12-21; ID: 93190535<br>Edward N. Luttwak - La grande strategia dell__039;impero romano" href="edition.php?id=137964517">La grande strategia dell’impero bizantino <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2187250</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Rizzoli</td>
<td><nobr>2010</nobr></td>
<td>Italian</td>
<td>0 / 547</td>
<td><nobr><a href="/file.php?id=93190535">1 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=479a398bab38c23068679c4f539cca20"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/479a398bab38c23068679c4f539cca20"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/479a398bab38c23068679c4f539cca20?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/479a398bab38c23068679c4f539cca20"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-02-21/2019-12-21; ID: 93190536<br>Edward N. Luttwak - La grande strategia dell__039;impero bizantino" href="edition.php?id=137964518">La grande strategia dell’impero romano <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2187251</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Rizzoli</td>
<td><nobr>2013</nobr></td>
<td>Italian</td>
<td>0 / 294</td>
<td><nobr><a href="/file.php?id=93190536">3 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=1b7b4c4fbfed87de5424ef7ad111e2fb"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/1b7b4c4fbfed87de5424ef7ad111e2fb"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/1b7b4c4fbfed87de5424ef7ad111e2fb?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/1b7b4c4fbfed87de5424ef7ad111e2fb"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-04-22/2020-04-22; ID: 93487967<br>" href="edition.php?id=138284273">拜占庭帝国大战略（思想会） <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2506963</span></nobr>

</td>
<td>爱德华•N.勒特韦克（Edward N. Luttwak）</td>
<td>社会科学文献出版社</td>
<td><nobr>2018</nobr></td>
<td>Chinese</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93487967">2 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=c96f62589115fa97d90629de418b1b22"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/c96f62589115fa97d90629de418b1b22"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/c96f62589115fa97d90629de418b1b22?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/c96f62589115fa97d90629de418b1b22"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-06-09/2020-06-12; ID: 93519466<br>" href="edition.php?id=138315936">Coup d'État: A Practical Handbook <i>Revised Edition</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-06-09/2020-06-12; ID: 93519466<br>" href="edition.php?id=138315936"><i><font color="green"> 9780674737266; 0674737261; 9780674969650; 0674969650; 9780674969667; 0674969669; 2015033858; 9782015033853</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2538631</span></nobr>

</td>
<td>Edward Luttwak</td>
<td>Harvard Uni Press</td>
<td><nobr>2016</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93519466">3 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=14b09955e9326fd656b103384f87824d"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/14b09955e9326fd656b103384f87824d"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/14b09955e9326fd656b103384f87824d?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/14b09955e9326fd656b103384f87824d"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-04-24; ID: 93556857<br>Ian Fletcher & Edward Luttwak - Free Trade Doesn't Work (mobi)" href="edition.php?id=138353832">Free trade doesn't work: what should replace it and why <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-04-24; ID: 93556857<br>Ian Fletcher & Edward Luttwak - Free Trade Doesn't Work (mobi)" href="edition.php?id=138353832"><i><font color="green"> 9780578048208; 0578048205; 9780578053325; 0578053322</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2576532</span></nobr>

</td>
<td>Luttwak, Edward;Fletcher, Ian</td>
<td>USBIC;U.S. Business and Industry Council</td>
<td><nobr>2010</nobr></td>
<td>English</td>
<td>0 / 323</td>
<td><nobr><a href="/file.php?id=93556857">863 kB</a></nobr></td>
<td>mobi</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=a269233e83e856ae2255be569b28ff27"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/a269233e83e856ae2255be569b28ff27"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/a269233e83e856ae2255be569b28ff27?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/a269233e83e856ae2255be569b28ff27"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2020-07-27; ID: 93637918<br>2009 Edward Luttwak - Grand Strategy of the Byzantine Empire_Rebgl" href="edition.php?id=138435160">The grand strategy of the Byzantine Empire <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2020-07-27; ID: 93637918<br>2009 Edward Luttwak - Grand Strategy of the Byzantine Empire_Rebgl" href="edition.php?id=138435160"><i><font color="green"> 9780674035195; 0674035194; 9780674054202; 0674054202; 9780674062078; 0674062078</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2657860</span></nobr>

</td>
<td>Luttwak, Edward N</td>
<td>The Belknap Press of Harvard University Press</td>
<td><nobr>2011</nobr></td>
<td>English</td>
<td>513 / vi, 498 Seiten ; 24 cm</td>
<td><nobr><a href="/file.php?id=93637918">3 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=bee3645f55ca6638c8df2640cfbefd5c"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/bee3645f55ca6638c8df2640cfbefd5c"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/bee3645f55ca6638c8df2640cfbefd5c?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/bee3645f55ca6638c8df2640cfbefd5c"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812241<br>Israeli Army" href="edition.php?id=138615421">Israeli Army, 1948-1973 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812241<br>Israeli Army" href="edition.php?id=138615421"><i><font color="green"> 0890115850; 9780890115855</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2837984</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td></td>
<td><nobr></nobr></td>
<td>English</td>
<td>411</td>
<td><nobr><a href="/file.php?id=93812241">13 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=5a7fe3e99559f2613683ad441c516c9f"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/5a7fe3e99559f2613683ad441c516c9f"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/5a7fe3e99559f2613683ad441c516c9f?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/5a7fe3e99559f2613683ad441c516c9f"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812247<br>Grand Strategy of Soviet Union" href="edition.php?id=138615428">Grand Strategy of Soviet Union <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812247<br>Grand Strategy of Soviet Union" href="edition.php?id=138615428"><i><font color="green"> 0312342586; 9780312342586</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2837990</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td></td>
<td><nobr></nobr></td>
<td>English</td>
<td>254</td>
<td><nobr><a href="/file.php?id=93812247">8 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=668086c38e26e5742c416b2312990180"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/668086c38e26e5742c416b2312990180"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/668086c38e26e5742c416b2312990180?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/668086c38e26e5742c416b2312990180"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812249<br>Endangered American Dream - How to Stop US from Becoming Third World Country and How to Win Geo-Economic Struggle for Industrial Supremacy" href="edition.php?id=138615430">Endangered American Dream - How to Stop US from Becoming Third World Country and How to Win Geo-Economic Struggle for Industrial Supremacy <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812249<br>Endangered American Dream - How to Stop US from Becoming Third World Country and How to Win Geo-Economic Struggle for Industrial Supremacy" href="edition.php?id=138615430"><i><font color="green"> 0671896679; 9780671896676</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2837992</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td></td>
<td><nobr></nobr></td>
<td>English</td>
<td>361</td>
<td><nobr><a href="/file.php?id=93812249">20 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=9983ebb041db3abf9221e1d109108a36"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/9983ebb041db3abf9221e1d109108a36"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/9983ebb041db3abf9221e1d109108a36?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/9983ebb041db3abf9221e1d109108a36"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812250<br>Dictionary of Modern War" href="edition.php?id=138615431">Dictionary of Modern War <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2837993</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td></td>
<td><nobr></nobr></td>
<td>English</td>
<td>284</td>
<td><nobr><a href="/file.php?id=93812250">13 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=3b8ab81426272927b4c1f275fc385841"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/3b8ab81426272927b4c1f275fc385841"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/3b8ab81426272927b4c1f275fc385841?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/3b8ab81426272927b4c1f275fc385841"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812253<br>Geopolitics Reader" href="edition.php?id=138615434">Geopolitics Reader <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812253<br>Geopolitics Reader" href="edition.php?id=138615434"><i><font color="green"> 0203444930; 9780203444931; 0203753178; 9780203753170; 041516270X; 9780415162708; 0415162718; 9780415162715</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2837996</span></nobr>

</td>
<td>Simon Dalby, Paul Routledge, Gearóid Ó Tuathail, Edward Luttwak</td>
<td></td>
<td><nobr></nobr></td>
<td>English</td>
<td>342</td>
<td><nobr><a href="/file.php?id=93812253">2 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=ee1bb788caf9cb3d05685e05145e3765"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/ee1bb788caf9cb3d05685e05145e3765"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/ee1bb788caf9cb3d05685e05145e3765?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/ee1bb788caf9cb3d05685e05145e3765"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812364<br>" href="edition.php?id=138615560">Virtual American Empire - War, Faith, and Power <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812364<br>" href="edition.php?id=138615560"><i><font color="green"> 9781412810395; 1412810396; 9781412810401; 141281040X</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2838111</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Transaction Publishers</td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93812364">809 kB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=6d0c47d4af6e4fc9770f4417df327549"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/6d0c47d4af6e4fc9770f4417df327549"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/6d0c47d4af6e4fc9770f4417df327549?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/6d0c47d4af6e4fc9770f4417df327549"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812365<br>" href="edition.php?id=138615561">Turbo-Capitalism - Winners and Losers in Global Economy <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812365<br>" href="edition.php?id=138615561"><i><font color="green"> 006093137X; 9780060931377</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2838112</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Harper Perennial</td>
<td><nobr>1998</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93812365">17 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d03661aa7b675e65f2af87000f137446"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d03661aa7b675e65f2af87000f137446"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d03661aa7b675e65f2af87000f137446?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d03661aa7b675e65f2af87000f137446"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812366<br>" href="edition.php?id=138615563">Strategic Power - Military Capabilities and Political Utility <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-11/2020-11-18; ID: 93812366<br>" href="edition.php?id=138615563"><i><font color="green"> 0803906595; 9780803906594</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2838113</span></nobr>

</td>
<td>Edward N. Luttwak</td>
<td>Sage Publications</td>
<td><nobr>1977</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93812366">3 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=031b725487bd8b0e6ca640dab87d43bd"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/031b725487bd8b0e6ca640dab87d43bd"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/031b725487bd8b0e6ca640dab87d43bd?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/031b725487bd8b0e6ca640dab87d43bd"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr></tbody></table><table>
  <tr>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
  </tr> 
  <tr>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
  </tr> 
  <tr>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
    <td><script type="text/javascript">
	atOptions = {
		'key' : '80ff16b446cdd16fda9f69edcec465d4',
		'format' : 'iframe',
		'height' : 60,
		'width' : 468,
		'params' : {}
	};
	document.write('<scr' + 'ipt type="text/javascript" src="http' + (location.protocol === 'https:' ? 's' : '') + '://inopportunefable.com/80ff16b446cdd16fda9f69edcec465d4/invoke.js"></scr' + 'ipt>');
</script></td>
  </tr> 
</table><div style="text-align: center;" class="paginator" id="paginator_example_bottom"></div><script type="text/javascript">paginator_example_bottom = new Paginator("paginator_example_bottom", 3, 25, 1, "/index.php?req=Luttwak&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><div class="modal fade text-dark" id="googlemodemodal" tabindex="-1" aria-labelledby="googlemodemodalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="googlemodemodalLabel">Google mode</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        
By default, the search searches for a set of marked fields containing all the words specified in the query in no particular order<br>
Advanced search mode (Google mode), allows you to set more precise search terms:<br>
- Quotes: "" - search exactly for the phrase as it is written in the database<br>
- Mask: * (min 3 chars)- search by part of a word<br>
- Excluding words: - (minus) - does not display records containing this word, also, these conditions can be combined.<br>
Example:<br>
"Physics and Chemistry" Basi * -technology<br>
means the title of the book contains the exact phrase "Physics and Chemistry", contains the word starting with Basi and does not contain the word technology.<br>
You can also search for a specific field or view mode that is not displayed for selection in the interface, syntax: field_name:value<br>
List of add. fields:<br>
For the Files tab:<br>
<i>md5</i><br>
<i>tth</i><br>
<i>sha1</i><br>
<i>sha256</i><br>
<i>crc32</i><br>
<i>edonkey</i><br>
<i>doi</i><br>

View modes:<br>
<i>mode:last</i> - last added entries (for a given object - series, authors, editions, etc.)<br>
<br>
<i>fmode:last</i> - last added files (for the given repository)<br>
<br>
Add. fields for object "editions" and "files":<br>
<i>issuevolume</i> - periodical volume<br>
<i>issuesid</i> - serial ID of the periodical<br>
<i>issuenumber</i> - the number (within the volume) of the periodical<br>
<i>issuetnumber</i> is the gross number of the periodical<br>
<i>issueynumber</i> - intra-annual issue of the periodical<br>
<i>year</i> - year<br>
<i>publisherid</i> - Publisher ID<br>
<i>authorid</i> - Author's ID<br>
<i>lang</i> - three-letter language code (ISO 639)<br>
<i>fsize</i> - filesize (MBytes), for example: fsize&gt;10, fsize&lt;20, fsize=15<br>
<i>ext</i> - File extenstion <br>
<i>booktopicid</i> - ID of the classifier for books<br>
<i>tags</i> - Теги (издание, работы, серия)<br>
<br>
Add. fields for object "series"<br>
<i>comtopicid</i> - ID of the classifier for comics<br>
<i>smtopicid</i> - ID of the classifier for scientific journals<br>
<i>magtopicid</i> - ID of the classifier for magazines<br>
<i>issn</i> - ISSN

      </div>
    </div>
  </div>
</div><nav class="navbar sticky-bottom navbar-expand-sm navbar-dark bg-secondary">
  <div class="collapse navbar-collapse" id="navbarCollapse">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
	    <a class="nav-link" href="#" data-toggle="modal" data-target="#dmcamodal">DMCA</a>
      </li>
      <li class="nav-item">
	    <a class="nav-link" href="#" data-toggle="modal" data-target="#aboutmodal">ABOUT</a>
      </li>
      <li class="nav-item">
	    <a class="nav-link" href="#" data-toggle="modal" data-target="#donatemodal" >DONATE</a>
      </li>
	
    </ul>
	<span class="navbar-text">Users online 5979</span>
  </div>
</nav>

<!-- Modal Donate -->
<div class="modal fade text-dark" id="donatemodal" tabindex="-1" aria-labelledby="donatemodalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="donatemodalLabel">Donate</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <a href="bitcoin://bc1qlv9lwa5vncm2jjrxyhddfcvu0z3u5vn0s9672r">Bitcoin</a>
	<br>
        <a href="monero:48WhyKv4D9x53SyDFNYuMsHsDzuHXEcht4mWoFtXtE3k4KZ3A7goi3CQWBQQZ3A8PSK7CpwnAFKLnfGiZTAbEpcaCQCghvN">Monero</a>
      </div>
    </div>
  </div>
</div>

<!-- Modal About -->
<div class="modal fade text-dark" id="aboutmodal" tabindex="-1" aria-labelledby="aboutmodalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="aboutmodalLabel">About</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">


<div id="about">
The Library Genesis aggregator is a community aiming at collecting and cataloging items descriptions for the most part of scientific, 
scientific and technical directions, as well as file metadata. In addition to the descriptions, 
the aggregator contains only links to third-party resources hosted by users. 
All information posted on the website is collected from publicly available public Internet resources and is intended solely for informational purposes.  
</div>
      </div>
    </div>
  </div>
</div>

<!-- Modal DMCA -->
<div class="modal fade text-dark" id="dmcamodal" tabindex="-1" aria-labelledby="dmcamodalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="dmcamodalLabel">About</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">

<div id="dmca">
Library Genesis - aggregator items is a website that collects and organizes online items from users. 
Item aggregation is done for fact-finding purposes, and website Library Genesis respects the rights of copyright holders and respect dcma.

     Removing Content From Library Genesis / DMCA Policy
     Library Genesis respects the intellectual property of others.
</div>

    <div class="dmca">
     If you believe that your copyrighted work has been copied in a way that constitutes copyright infringement and is accessible on this site, you may notify our copyright agent, as set forth in the Digital Millennium Copyright Act of 1998 (DMCA). For your complaint to be valid under the DMCA, you must provide the following information when providing notice of the claimed copyright infringement:
</div>
    <div class="dmca">
     * A physical or electronic signature of a person authorized to act on behalf of the copyright owner Identification of the copyrighted work claimed to have been infringed <br />
     * Identification of the material that is claimed to be infringing or to be the subject of the infringing activity and that is to be removed <br />
     * Information reasonably sufficient to permit the service provider to contact the complaining party, such as an address, telephone number, and, if available, an electronic mail address <br />
     * A statement that the complaining party "in good faith believes that use of the material in the manner complained of is not authorized by the copyright owner, its agent, or law" <br />
     * A statement that the "information in the notification is accurate", and "under penalty of perjury, the complaining party is authorized to act on behalf of the owner of an exclusive right that is allegedly infringed" <br />
     The above information must be submitted as a written, faxed or emailed notification to the following Designated Agent: ianzlib@protonmail.com. Appeals will be reviewed within 72 hours.</div>


      </div>
    </div>
  </div>
</div>


	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.5/dist/popper.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
	<script src="/js/form-validation.js"></script>
	<script>
$('[data-toggle="tooltip"]').tooltip();
$('.btn-tooltip-bottom').tooltip({
    placement: 'bottom'
});
</script>

</body>
</html>