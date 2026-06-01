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
   <a class="navbar-brand" href="setlang.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&lang=ru">RU</a>
</nav>
<form class="card p-2 needs-validation" novalidate id="formlibgen" action="index.php" enctype="multipart/form-data" METHOD="GET">
<div class="input-group mb-3" >
	<input autofocus type="text" class="form-control" placeholder="Input value" name="req" aria-label="input text" aria-describedby="button-addon2" value="Chris Wickham" required>
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
				<input type="checkbox" checked class="column-input" id="objs" name="objects[]" value="s">
				<label class="column-label" for="objs">Series</label>
				<input type="checkbox" checked class="column-input" id="obja" name="objects[]" value="a">
				<label class="column-label" for="obja">Authors</label>
				<input type="checkbox" checked class="column-input" id="objp" name="objects[]" value="p">
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
 <a class="nav-link active " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f">Files <span class="badge badge-primary">97</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=e">Editions <span class="badge badge-primary">105</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=s">Series <span class="badge badge-primary">0</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=a">Authors <span class="badge badge-primary">0</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=p">Publishers <span class="badge badge-primary">0</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=w">Works</a>
</li><li class="navbar-right" style="float: right !important;"><a class="nav-link" href="/json.php?object=f&ids=91408535,91442655,91609596,91758803,91799685,91823502,91842328,91847613,91988884,92305096,92340575,92587171,92632893,93164698,93248235,93293431,93342875,93385610,93425813,93475233,93685563,93685566,93697346,93710394,93814247,93817636,93882703,93932052,97475133,97475134,97512353,97512354,97512356,97512357,98075727,99251342,99413045,99730795,100789808,100891154,101174848,101293078,103696012,103998343,104000058,104039448,104039456,104058007,104996508,106954765,106959799,111929237,112039419,112887743,112888139,112888590,112888601,112888693,112889533,113606112,114095415,114672023,114673510,114673826,114674651,115588355,110499120,89719456,91525258,92695032,93150137,93568566,93685564,93685565,93685567,93685568,93685569,93685570,97512355,99008790,101217806,101217826,103807594,108650009,109409198,109409202,109409219,109409226,109437925,109790771,110141209,110403009,110467446,110536046,110996698,113473312,115174990"><font color="black">JSON</font></a></li> </ul><div style="text-align: center;" class="paginator" id="paginator_example_top"></div><script type="text/javascript">paginator_example_top = new Paginator("paginator_example_top", 4, 25, 1, "/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><table class="table  table-striped" id="tablelibgen"><thead><tr>

<th scope="col" class="first_col"><nobr>
ID <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=f_id&ordermode=asc">&#8597</a> 
Time add. <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=time_added&ordermode=asc">&#8597</a> 
Title <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=title&ordermode=asc">&#8597</a> 
Series <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=series&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Author(s) <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=author&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Publisher <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=publisher&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Year <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=year&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Language</th>
<th scope="col">Pages</th>
<th scope="col"><nobr>Size  <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=filesize&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Ext. <a href="/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=extension&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Mirrors</th>
</tr></thead><tbody><tr>

<td><b>New Perspectives on the Past<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2010-08-30/2025-09-20; ID: 91408535<br>690920d3b188d3673e7e5e63b4fc9749" href="edition.php?id=136083097"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2010-08-30/2025-09-20; ID: 91408535<br>690920d3b188d3673e7e5e63b4fc9749" href="edition.php?id=136083097">Social Memory (New Perspectives on the Past) <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2010-08-30/2025-09-20; ID: 91408535<br>690920d3b188d3673e7e5e63b4fc9749" href="edition.php?id=136083097"><i><font color="green"> 063116619X; 9780631166191</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 305830</span></nobr>

</td>
<td>James Fentress, Chris Wickham</td>
<td>Blackwell Pub</td>
<td><nobr>1992</nobr></td>
<td>English</td>
<td>245 / 245</td>
<td><nobr><a href="/file.php?id=91408535">25 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=690920d3b188d3673e7e5e63b4fc9749"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/690920d3b188d3673e7e5e63b4fc9749"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/690920d3b188d3673e7e5e63b4fc9749?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/690920d3b188d3673e7e5e63b4fc9749"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/690920d3b188d3673e7e5e63b4fc9749"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-01-24/2022-03-25; ID: 91442655<br>Wickham - Framing the Early Middle Ages ~ Europe and the Mediterranean, 400-800 0-19-926449-X 1 3 5 7 9 10 8 6 4 2" href="edition.php?id=136120041">Framing the Early Middle Ages: Europe and the Mediterranean, 400-800 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-01-24/2022-03-25; ID: 91442655<br>Wickham - Framing the Early Middle Ages ~ Europe and the Mediterranean, 400-800 0-19-926449-X 1 3 5 7 9 10 8 6 4 2" href="edition.php?id=136120041"><i><font color="green"> 019926449X; 9780199264490</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 342774</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Oxford University Press, USA</td>
<td><nobr>2005</nobr></td>
<td>English</td>
<td>1019 / 1019</td>
<td><nobr><a href="/file.php?id=91442655">8 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=2a14f18ac023705fdab32f05e4ee4004"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/2a14f18ac023705fdab32f05e4ee4004"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/2a14f18ac023705fdab32f05e4ee4004?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/2a14f18ac023705fdab32f05e4ee4004"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/2a14f18ac023705fdab32f05e4ee4004"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-30; ID: 91609596<br>_72054.a158d2d62593d5cc502243025ba6decb" href="edition.php?id=136294480">Framing the Early Middle Ages: Europe and the Mediterranean, 400-800 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-06-04/2021-09-30; ID: 91609596<br>_72054.a158d2d62593d5cc502243025ba6decb" href="edition.php?id=136294480"><i><font color="green"> 019926449X; 9780199264490; 9781429469975; 1429469978</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 517213</span></nobr>

</td>
<td>Chris Wickham</td>
<td></td>
<td><nobr>2005</nobr></td>
<td>English</td>
<td>1019 / 1018</td>
<td><nobr><a href="/file.php?id=91609596">8 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=a158d2d62593d5cc502243025ba6decb"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/a158d2d62593d5cc502243025ba6decb"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/a158d2d62593d5cc502243025ba6decb?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/a158d2d62593d5cc502243025ba6decb"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/a158d2d62593d5cc502243025ba6decb"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-08-31/2019-12-21; ID: 91758803<br>_409316.9c08d0c522ac69637eec33dd6cdfa353" href="edition.php?id=136454441">Framing the past: the historiography of German cinema and television <i>1st</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-08-31/2019-12-21; ID: 91758803<br>_409316.9c08d0c522ac69637eec33dd6cdfa353" href="edition.php?id=136454441"><i><font color="green"> 0809317567; 9780809317561</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 677174</span></nobr>

</td>
<td>Bruce Arthur Murray, Chris Wickham</td>
<td>SIU Press</td>
<td><nobr>1992</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=91758803">825 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=9c08d0c522ac69637eec33dd6cdfa353"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/9c08d0c522ac69637eec33dd6cdfa353"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/9c08d0c522ac69637eec33dd6cdfa353?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/9c08d0c522ac69637eec33dd6cdfa353"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/9c08d0c522ac69637eec33dd6cdfa353"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><b>New Perspectives on the Past<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2019-12-21; ID: 91799685<br>_514375.01ea2fcfc900d82a951b9319861e40c0" href="edition.php?id=136500106"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2019-12-21; ID: 91799685<br>_514375.01ea2fcfc900d82a951b9319861e40c0" href="edition.php?id=136500106">Social Memory   <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2019-12-21; ID: 91799685<br>_514375.01ea2fcfc900d82a951b9319861e40c0" href="edition.php?id=136500106"><i><font color="green"> 0631166181; 9780631166184; 063116619X; 9780631166191</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 722839</span></nobr>

</td>
<td>James Fentress, Chris Wickham</td>
<td>Blackwell</td>
<td><nobr>1992</nobr></td>
<td>English</td>
<td>241 / 241</td>
<td><nobr><a href="/file.php?id=91799685">6 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=01ea2fcfc900d82a951b9319861e40c0"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/01ea2fcfc900d82a951b9319861e40c0"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/01ea2fcfc900d82a951b9319861e40c0?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/01ea2fcfc900d82a951b9319861e40c0"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/01ea2fcfc900d82a951b9319861e40c0"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2022-03-25; ID: 91823502<br>_476581.6cfa3df6ed21dcd76f7a0e5f7d350168" href="edition.php?id=136527086">City and Countryside in Late Medieval and Renaissance Italy: Essays Presented to Philip Jones <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2022-03-25; ID: 91823502<br>_476581.6cfa3df6ed21dcd76f7a0e5f7d350168" href="edition.php?id=136527086"><i><font color="green"> 1852850353; 9781852850357</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 749819</span></nobr>

</td>
<td>Trevor Dean; Chris Wickham</td>
<td>Hambledon Continuum</td>
<td><nobr>2003</nobr></td>
<td>English</td>
<td>218 / 218</td>
<td><nobr><a href="/file.php?id=91823502">9 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=6cfa3df6ed21dcd76f7a0e5f7d350168"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/6cfa3df6ed21dcd76f7a0e5f7d350168"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/6cfa3df6ed21dcd76f7a0e5f7d350168?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/6cfa3df6ed21dcd76f7a0e5f7d350168"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/6cfa3df6ed21dcd76f7a0e5f7d350168"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><b>New Studies in Medieval History<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2022-03-25; ID: 91842328<br>_454396.c3fba061a48ff0e8a11a616e3c861ba2" href="edition.php?id=136548610"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2022-03-25; ID: 91842328<br>_454396.c3fba061a48ff0e8a11a616e3c861ba2" href="edition.php?id=136548610">Early Medieval Italy: Central Power and Local Society 400-1000 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2022-03-25; ID: 91842328<br>_454396.c3fba061a48ff0e8a11a616e3c861ba2" href="edition.php?id=136548610"><i><font color="green"> 0389202177; 9780389202172</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 771343</span></nobr>

</td>
<td>Chris Wickham</td>
<td>The Macmillan Press Ltd</td>
<td><nobr>1981</nobr></td>
<td>English</td>
<td>256 / 256</td>
<td><nobr><a href="/file.php?id=91842328">31 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=c3fba061a48ff0e8a11a616e3c861ba2"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/c3fba061a48ff0e8a11a616e3c861ba2"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/c3fba061a48ff0e8a11a616e3c861ba2?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/c3fba061a48ff0e8a11a616e3c861ba2"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/c3fba061a48ff0e8a11a616e3c861ba2"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2019-12-21; ID: 91847613<br>_446079.dcb87a3d68168a22c9c83a1033f17f1a" href="edition.php?id=136554605">The Inheritance of Rome: A History of Europe from 400 to 1000   <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2019-12-21; ID: 91847613<br>_446079.dcb87a3d68168a22c9c83a1033f17f1a" href="edition.php?id=136554605"><i><font color="green"> 9780141908533; 014190853X</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 777338</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Allen Lane</td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>0 / 656</td>
<td><nobr><a href="/file.php?id=91847613">6 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=dcb87a3d68168a22c9c83a1033f17f1a"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/dcb87a3d68168a22c9c83a1033f17f1a"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/dcb87a3d68168a22c9c83a1033f17f1a?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/dcb87a3d68168a22c9c83a1033f17f1a"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/dcb87a3d68168a22c9c83a1033f17f1a"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2013-06-24/2021-10-05; ID: 91988884<br>9780191514197" href="edition.php?id=136708444">Framing the early Middle Ages : Europe and the Mediterranean 400-800 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2013-06-24/2021-10-05; ID: 91988884<br>9780191514197" href="edition.php?id=136708444"><i><font color="green"> 019926449X; 9780199264490; 9780199212965; 0199212961; 9780191514197; 0191514195</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 931177</span></nobr>

</td>
<td>Chris Wickham.</td>
<td>Oxford University Press</td>
<td><nobr>2005.</nobr></td>
<td>English</td>
<td>1019 / xxviii, 990 p. : maps ; 24 cm.</td>
<td><nobr><a href="/file.php?id=91988884">9 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=0077dd02579b1ffdd9df4083751dbca4"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/0077dd02579b1ffdd9df4083751dbca4"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/0077dd02579b1ffdd9df4083751dbca4?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/0077dd02579b1ffdd9df4083751dbca4"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/0077dd02579b1ffdd9df4083751dbca4"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-10-05/2021-10-06; ID: 92305096<br>a0a348909cc7e5baf2ecaff174a9bef5-ocr" href="edition.php?id=136085932">Framing the Early Middle Ages: Europe and the Mediterranean, 400-800 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-10-05/2021-10-06; ID: 92305096<br>a0a348909cc7e5baf2ecaff174a9bef5-ocr" href="edition.php?id=136085932"><i><font color="green"> 9780199212965; 0199212961</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1254892</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Oxford University Press, USA</td>
<td><nobr>2007</nobr></td>
<td>English</td>
<td>1019 / 1019</td>
<td><nobr><a href="/file.php?id=92305096">8 MB</a></nobr></td>
<td>djvu</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=dfb4054b0624cea3e91ce044fe4e61a9"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/dfb4054b0624cea3e91ce044fe4e61a9"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/dfb4054b0624cea3e91ce044fe4e61a9?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/dfb4054b0624cea3e91ce044fe4e61a9"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/dfb4054b0624cea3e91ce044fe4e61a9"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><b>Oxford Studies in Medieval European History<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-11-09/2021-10-06; ID: 92340575<br>Medieval Rome Stability and Crisis of a City, 900-1150-978–0–19–968496–0" href="edition.php?id=137067911"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-11-09/2021-10-06; ID: 92340575<br>Medieval Rome Stability and Crisis of a City, 900-1150-978–0–19–968496–0" href="edition.php?id=137067911">Medieval Rome: Stability and Crisis of a City, 900-1150 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2014-11-09/2021-10-06; ID: 92340575<br>Medieval Rome Stability and Crisis of a City, 900-1150-978–0–19–968496–0" href="edition.php?id=137067911"><i><font color="green"> 0199684960; 9780199684960</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1290644</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Oxford University Press</td>
<td><nobr>2015</nobr></td>
<td>English</td>
<td>530 / 512</td>
<td><nobr><a href="/file.php?id=92340575">9 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=bc0ff11b30db1dd05d8c40e7dc510383"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/bc0ff11b30db1dd05d8c40e7dc510383"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/bc0ff11b30db1dd05d8c40e7dc510383?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/bc0ff11b30db1dd05d8c40e7dc510383"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/bc0ff11b30db1dd05d8c40e7dc510383"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><b>Lawrence Stone Lectures<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-09-26/2022-03-25; ID: 92587171<br>Sleepwalking into a New World" href="edition.php?id=137337938"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-09-26/2022-03-25; ID: 92587171<br>Sleepwalking into a New World" href="edition.php?id=137337938">Sleepwalking into a New World: The Emergence of Italian City Communes in the Twelfth Century <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1560671</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Princeton University Press</td>
<td><nobr>2015</nobr></td>
<td>English</td>
<td>320 / 320</td>
<td><nobr><a href="/file.php?id=92587171">7 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=062c03c3509bb7a6b249969bdc1a15e6"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/062c03c3509bb7a6b249969bdc1a15e6"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/062c03c3509bb7a6b249969bdc1a15e6?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/062c03c3509bb7a6b249969bdc1a15e6"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/062c03c3509bb7a6b249969bdc1a15e6"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><b>Oxford Studies in Medieval European<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-01-20/2022-03-09; ID: 92632893<br>Chris Wickham;Medieval Rome" href="edition.php?id=137390883"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-01-20/2022-03-09; ID: 92632893<br>Chris Wickham;Medieval Rome" href="edition.php?id=137390883">Medieval Rome. Stability and Crisis of a City, 900-1150 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-01-20/2022-03-09; ID: 92632893<br>Chris Wickham;Medieval Rome" href="edition.php?id=137390883"><i><font color="green"> 9780199684960; 0199684960</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1613616</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Oxford University Press</td>
<td><nobr>2015</nobr></td>
<td>English</td>
<td>530</td>
<td><nobr><a href="/file.php?id=92632893">10 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=9ee30195240fd8a74d1a1880e4c62040"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/9ee30195240fd8a74d1a1880e4c62040"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/9ee30195240fd8a74d1a1880e4c62040?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/9ee30195240fd8a74d1a1880e4c62040"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-12-02/2019-12-21; ID: 93164698<br>Medieval Europe - Christopher Wickham" href="edition.php?id=137936474">Medieval Europe <i>1st</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2017-12-02/2019-12-21; ID: 93164698<br>Medieval Europe - Christopher Wickham" href="edition.php?id=137936474"><i><font color="green"> 0300208340; 9780300208344</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2159207</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Yale University Press</td>
<td><nobr>2016</nobr></td>
<td>English</td>
<td>0 / 0</td>
<td><nobr><a href="/file.php?id=93164698">5 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=1789b41b84c5c577f99b10b7363da7a7"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/1789b41b84c5c577f99b10b7363da7a7"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/1789b41b84c5c577f99b10b7363da7a7?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/1789b41b84c5c577f99b10b7363da7a7"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-08-09/2022-04-02; ID: 93248235<br>Wickham Chris - Europa En La Edad Media - Una Nueva Interpretacion" href="edition.php?id=138024567">Europa en la Edad Media: Una Nueva Interpretacion <i>1st</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-08-09/2022-04-02; ID: 93248235<br>Wickham Chris - Europa En La Edad Media - Una Nueva Interpretacion" href="edition.php?id=138024567"><i><font color="green"> 9788417067151; 8417067159</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2247300</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Crítica</td>
<td><nobr>2017</nobr></td>
<td>Spanish</td>
<td>0 / 1625</td>
<td><nobr><a href="/file.php?id=93248235">6 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=ab670a1c8bb5620b0c08be5e157aa67d"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/ab670a1c8bb5620b0c08be5e157aa67d"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/ab670a1c8bb5620b0c08be5e157aa67d?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/ab670a1c8bb5620b0c08be5e157aa67d"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-12-08/2019-12-21; ID: 93293431<br>Chris Wickham - L__039;eredità di Roma (Laterza, 2016)" href="edition.php?id=138073361">L’eredità di Roma. Storia d’Europa dal 400 al 1000 d.C. <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2296094</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Laterza</td>
<td><nobr>2016</nobr></td>
<td>Italian</td>
<td>0 / 0</td>
<td><nobr><a href="/file.php?id=93293431">9 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=45a10fcdbeff5061cb275966cb55209b"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/45a10fcdbeff5061cb275966cb55209b"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/45a10fcdbeff5061cb275966cb55209b?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/45a10fcdbeff5061cb275966cb55209b"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2019-04-09/2019-12-21; ID: 93342875<br>wickham_chris_medieval_europe" href="edition.php?id=138126217">Medieval Europe <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2348950</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Yale University Press</td>
<td><nobr>2016</nobr></td>
<td>English</td>
<td>377 / 377</td>
<td><nobr><a href="/file.php?id=93342875">80 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=5348b88b9d9d2ba9c7485dfc855a4203"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/5348b88b9d9d2ba9c7485dfc855a4203"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/5348b88b9d9d2ba9c7485dfc855a4203?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/5348b88b9d9d2ba9c7485dfc855a4203"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2019-08-01/2019-12-21; ID: 93385610<br>Chris-Wickham-The-Inheritance-of-Rome_-A-History-of-Europe-from-400-to-1000-Allen-Lane-_2009_" href="edition.php?id=138171485">The Inheritance of Rome: A History of Europe from 400 to 1000 <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2394218</span></nobr>

</td>
<td>Chris Wickham</td>
<td></td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>808 / 808</td>
<td><nobr><a href="/file.php?id=93385610">6 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=5990efa62cadb01dcc0be8e7439d7e55"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/5990efa62cadb01dcc0be8e7439d7e55"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/5990efa62cadb01dcc0be8e7439d7e55?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/5990efa62cadb01dcc0be8e7439d7e55"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2019-11-17/2019-12-21; ID: 93425813<br>merged (pdf.io) (2)" href="edition.php?id=138216081">The Inheritance of Rome: A History of Europe from 400 to 1000 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2019-11-17/2019-12-21; ID: 93425813<br>merged (pdf.io) (2)" href="edition.php?id=138216081"><i><font color="green"> 9780141908533; 014190853X</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2438814</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Penguin Books</td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>749 / 749</td>
<td><nobr><a href="/file.php?id=93425813">8 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=67dec56bd37d7a107368c42fb7274753"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/67dec56bd37d7a107368c42fb7274753"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/67dec56bd37d7a107368c42fb7274753?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/67dec56bd37d7a107368c42fb7274753"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b>Sekrety Historii<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-03-28/2024-12-16; ID: 93475233<br>WICKHAM, Chris - Średniowieczna Europa" href="edition.php?id=138271377"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-03-28/2024-12-16; ID: 93475233<br>WICKHAM, Chris - Średniowieczna Europa" href="edition.php?id=138271377">Średniowieczna Europa <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-03-28/2024-12-16; ID: 93475233<br>WICKHAM, Chris - Średniowieczna Europa" href="edition.php?id=138271377"><i><font color="green"> 9788377739570; 8377739577; 9788377739587; 8377739585</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2494109</span></nobr>

</td>
<td>Chris Wickham</td>
<td>RM</td>
<td><nobr>2018</nobr></td>
<td>Polish</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93475233">6 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d0b2af3f3f7c7c6dd974b97f116779c1"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d0b2af3f3f7c7c6dd974b97f116779c1"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d0b2af3f3f7c7c6dd974b97f116779c1?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d0b2af3f3f7c7c6dd974b97f116779c1"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-03-25; ID: 93685563<br>Framing the Early Middle Ages - Wickham, Chris_253B" href="edition.php?id=138482867">Framing the early Middle Ages: Europe and the Mediterranean 400-800 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-03-25; ID: 93685563<br>Framing the Early Middle Ages - Wickham, Chris_253B" href="edition.php?id=138482867"><i><font color="green"> 019926449X; 9780199264490; 0199212961; 9780199212965</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2705567</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Oxford University Press</td>
<td><nobr>2007;2005</nobr></td>
<td>English</td>
<td>0 / xxviii, 990 pages : illustrations, maps ; 24 cm</td>
<td><nobr><a href="/file.php?id=93685563">18 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d130fbdeb7229f80a4cf1eb7adc79cb0"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d130fbdeb7229f80a4cf1eb7adc79cb0"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d130fbdeb7229f80a4cf1eb7adc79cb0?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d130fbdeb7229f80a4cf1eb7adc79cb0"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-03-25; ID: 93685566<br>Medieval Europe - Wickham, Chris_253B" href="edition.php?id=138482870">Medieval Europe <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-07-26/2022-03-25; ID: 93685566<br>Medieval Europe - Wickham, Chris_253B" href="edition.php?id=138482870"><i><font color="green"> 9780300208344; 0300208340; 9780300228823; 0300228821</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2705570</span></nobr>

</td>
<td>Chris Wickham</td>
<td>Yale University Press</td>
<td><nobr>2017</nobr></td>
<td>English</td>
<td>377 / vii, 335 pages, 24 pages de planches non numérotées : illustrations, cartes ; 25 cm</td>
<td><nobr><a href="/file.php?id=93685566">79 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=12b491ac6b5bb8f7084da9ecf57e8472"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/12b491ac6b5bb8f7084da9ecf57e8472"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/12b491ac6b5bb8f7084da9ecf57e8472?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/12b491ac6b5bb8f7084da9ecf57e8472"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-08-06/2020-08-09; ID: 93697346<br>" href="edition.php?id=138494715">Europa en la Edad Media <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2717440</span></nobr>

</td>
<td>Chris Wickham</td>
<td>ePubLibre</td>
<td><nobr>2017</nobr></td>
<td>Spanish</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93697346">10 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=0866fdfe6ea1dbf4d711a0f5c99e769d"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/0866fdfe6ea1dbf4d711a0f5c99e769d"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/0866fdfe6ea1dbf4d711a0f5c99e769d?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/0866fdfe6ea1dbf4d711a0f5c99e769d"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-08-22/2021-10-02; ID: 93710394<br>Chris Wickham;Europa en la Edad Media;;;ePubLibre;2016;;;Spanish" href="edition.php?id=138507914">Europa en la Edad Media <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2730624</span></nobr>

</td>
<td>Chris Wickham</td>
<td>ePubLibre</td>
<td><nobr>2016</nobr></td>
<td>Spanish</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93710394">6 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=9575cbb9cc99ba15baaf52fc9f1a38ff"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/9575cbb9cc99ba15baaf52fc9f1a38ff"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/9575cbb9cc99ba15baaf52fc9f1a38ff?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/9575cbb9cc99ba15baaf52fc9f1a38ff"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b>Frónesis<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-15/2020-11-19; ID: 93814247<br>" href="edition.php?id=138617389"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-15/2020-11-19; ID: 93814247<br>" href="edition.php?id=138617389">Memoria social <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2020-11-15/2020-11-19; ID: 93814247<br>" href="edition.php?id=138617389"><i><font color="green"> 9788437620831; 843762083X</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2840023</span></nobr>

</td>
<td>James Fentress; Chris Wickham</td>
<td>Cátedra / Universidad de Valencia</td>
<td><nobr>2003</nobr></td>
<td>Spanish</td>
<td>0</td>
<td><nobr><a href="/file.php?id=93814247">9 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=4ac4e7decd6f24fbfc98b2bbfb710638"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/4ac4e7decd6f24fbfc98b2bbfb710638"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/4ac4e7decd6f24fbfc98b2bbfb710638?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/4ac4e7decd6f24fbfc98b2bbfb710638"><span class="badge badge-primary">4</span></a> </nobr></td>
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
</table><div style="text-align: center;" class="paginator" id="paginator_example_bottom"></div><script type="text/javascript">paginator_example_bottom = new Paginator("paginator_example_bottom", 4, 25, 1, "/index.php?req=Chris+Wickham&columns%5B%5D=a&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=a&objects%5B%5D=s&objects%5B%5D=p&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><div class="modal fade text-dark" id="googlemodemodal" tabindex="-1" aria-labelledby="googlemodemodalLabel" aria-hidden="true">
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
	<span class="navbar-text">Users online 5939</span>
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