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
   <a class="navbar-brand" href="setlang.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&lang=ru">RU</a>
</nav>
<form class="card p-2 needs-validation" novalidate id="formlibgen" action="index.php" enctype="multipart/form-data" METHOD="GET">
<div class="input-group mb-3" >
	<input autofocus type="text" class="form-control" placeholder="Input value" name="req" aria-label="input text" aria-describedby="button-addon2" value="Wickham" required>
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
 <a class="nav-link active " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f">Files <span class="badge badge-primary">350</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=e">Editions <span class="badge badge-primary">725</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=s">Series</a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=a">Authors <span class="badge badge-primary">10</span></a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=p">Publishers</a>
</li><li class="nav-item">
 <a class="nav-link  " href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=w">Works</a>
</li><li class="navbar-right" style="float: right !important;"><a class="nav-link" href="/json.php?object=f&ids=91694969,91846187,93287082,102463349,103801171,115064306,115064308,115064309,115064310,115064311,115075504,115077592,115077605,115078341,115081372,115100487,28133799,51552499,55170347,56000218,58062507,60863200,68163437,73429585,77214636,78409236,89719456,90510331,91351172,91387632,91408535,91442655,91487096,91494834,91497298,91521682,91525258,91537257,91547983,91548111,91587580,91593985,91609596,91630625,91659317,91710301,91710365,91711454,91711457,91711460,91711464,91734865,91755186,91758803,91772621,91781803,91799685,91803689,91806066,91823502,91833571,91835873,91842328,91847613,91869517,91898981,91986908,91988884,92149033,92305096,92336617,92340575,92356291,92358028,92362342,92370983,92370984,92424649,92441292,92512369,92513769,92559132,92559857,92585439,92587171,92626987,92630755,92632893,92658706,92695032,92720009,93146572,93150137,93150179,93164698,93168523,93188900,93194307,93220355,93232187,93248235,93255164,93259773,93293431,93342615,93342875,93343030,93385610,93418404,93425813,93437551,93472937,93475233,93479250,93545236,93545287,93568566,93607770,93611306,93652337,93652338,93660793,93660794,93685563,93685564,93685565,93685566,93685567,93685568,93685569,93685570,93685571,93685572,93685573,93685574,93685575,93685576,93697346,93710394,93814247,93817636,93822328,93825842,93829417,93831629,93833531,93839680,93882703,93903926,93925820,93932052,93933874,93937824,93972571,93978439,93978440,94013720,94048475,94055507,94055779,94056330,94058149,96765965,97469392,97475133,97475134,97512353,97512354,97512355,97512356,97512357,97512358,97801365,97917935,97979993,98042824,98075727,98272727,98279912,98404536,98508087,99008790,99011097,99209042,99213341,99251342,99277992,99299304,99413045,99419812,99423393,99428041,99430108,99730795,99771399,100175248,100258492,100650332,100789808,100891154,101174848,101217806,101217826,101291766,101293078,101304085,101926133,101977095,102100779,102137976,102427851,102463252,102496755,102857658,102858091,102878657,103624101,103632793,103636435,103641413,103678030,103684273,103684274,103685453,103685459,103696012,103758819,103782228,103807594,103905179,103998343,103998387,104000058,104023163,104024362,104039448,104039456,104058007,104869587,104904802,104996508,105236612,106110478,106641178,106699805,106707377,106954765,106959799,107048614,107144666,107144667,107732340,108382949,108468773,108471081,108512719,108520085,108591077,108591536,108608655,108644931,108650009,108731453,108879282,108902053,108933222,109060285,109099605,109273250,109279035,109315719,109405140,109405862,109409198,109409202,109409219,109409226,109417379,109437925,109515611,109595051,109613720,109741627,109744915,109775073,109790771,109802538,109804664,109871486,109904938,109930778,109963364,109971076,110022017,110141209,110241048,110360967,110403009,110425278,110467446,110499120,110529340,110536046,110640703,110696121,110734889,110766428,110814174,110825072,110830894,110973117,110973118,110996698,111929237,112039419,112060325,112485798,112808529,112843820,112887743,112888139,112888590,112888601,112888693,112889533,113473312,113606112,113722611,114095415,114663196,114672023,114673510,114673826,114674651,114713668,114713669,114713671,114713672,114713673,114823336,114963965,115174990,115299071,115529060,115529061,115536841,115581604,115588355,115600749,115793362"><font color="black">JSON</font></a></li> </ul><div style="text-align: center;" class="paginator" id="paginator_example_top"></div><script type="text/javascript">paginator_example_top = new Paginator("paginator_example_top", 14, 25, 1, "/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><table class="table  table-striped" id="tablelibgen"><thead><tr>

<th scope="col" class="first_col"><nobr>
ID <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=f_id&ordermode=asc">&#8597</a> 
Time add. <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=time_added&ordermode=asc">&#8597</a> 
Title <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=title&ordermode=asc">&#8597</a> 
Series <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=series&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Author(s) <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=author&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Publisher <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=publisher&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Year <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=year&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Language</th>
<th scope="col">Pages</th>
<th scope="col"><nobr>Size  <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=filesize&ordermode=asc">&#8597</a></nobr></th>
<th scope="col"><nobr>Ext. <a href="/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=extension&ordermode=asc">&#8597</a></nobr></th>
<th scope="col">Mirrors</th>
</tr></thead><tbody><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2011-08-31/2019-12-21; ID: 91694969<br>_321851.2a8a7ed50082d3cf1c0a3502dc7a9883" href="edition.php?id=136384190">El Orinoco en dos direcciones: Relatos de viajes de Sir Henry Alexander Wickham (1869-1870) y Jules Crevaux (1880-1881) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 606923</span></nobr>

</td>
<td>Henry Alexander Wickham, Jules Crevaux, Miguel Ángel Perera</td>
<td>Fundación Cultural Orinoco</td>
<td><nobr>1988</nobr></td>
<td>Spanish</td>
<td>300 / 333</td>
<td><nobr><a href="/file.php?id=91694969">94 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=2a8a7ed50082d3cf1c0a3502dc7a9883"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/2a8a7ed50082d3cf1c0a3502dc7a9883"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/2a8a7ed50082d3cf1c0a3502dc7a9883?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/2a8a7ed50082d3cf1c0a3502dc7a9883"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/2a8a7ed50082d3cf1c0a3502dc7a9883"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2021-10-03; ID: 91846187<br>_444774.d5d4fe5a160febdea85b52bf73ed5a91" href="edition.php?id=136552967">Management Consulting: Delivering an Effective Project <i>3rd Edition</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2012-02-04/2021-10-03; ID: 91846187<br>_444774.d5d4fe5a160febdea85b52bf73ed5a91" href="edition.php?id=136552967"><i><font color="green"> 0273711849; 9780273711841</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 775700</span></nobr>

</td>
<td>Philip A. Wickham, Louise Wickham</td>
<td>Prentice Hall</td>
<td><nobr>2008</nobr></td>
<td>English</td>
<td>337 / 337</td>
<td><nobr><a href="/file.php?id=91846187">3 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=d5d4fe5a160febdea85b52bf73ed5a91"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/d5d4fe5a160febdea85b52bf73ed5a91"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/d5d4fe5a160febdea85b52bf73ed5a91?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/d5d4fe5a160febdea85b52bf73ed5a91"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/d5d4fe5a160febdea85b52bf73ed5a91"><span class="badge badge-primary">5</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-11-26/2019-12-21; ID: 93287082<br>Practical Java Machine Learning_ Projects - Mark Wickham" href="edition.php?id=138066946">Practical Java Machine Learning: Projects with Google Cloud Platform and Amazon Web Services <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2289679</span></nobr>

</td>
<td>Mark Wickham [Mark Wickham]</td>
<td>Apress</td>
<td><nobr>2018</nobr></td>
<td>English</td>
<td>0 / 0</td>
<td><nobr><a href="/file.php?id=93287082">6 MB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=db41759abf0aef82c1b6163a75db5466"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/db41759abf0aef82c1b6163a75db5466"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/db41759abf0aef82c1b6163a75db5466?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/db41759abf0aef82c1b6163a75db5466"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2023-07-13/2023-07-13; ID: 102463349<br>John A. Wickham - Korea on the Brink: A Memoir of Political Intrigue and Military Crisis (2000, Potomac Books Inc.)" href="edition.php?id=146214060">Korea on the Brink: A Memoir of Political Intrigue and Military Crisis <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2023-07-13/2023-07-13; ID: 102463349<br>John A. Wickham - Korea on the Brink: A Memoir of Political Intrigue and Military Crisis (2000, Potomac Books Inc.)" href="edition.php?id=146214060"><i><font color="green"> 1574882902; 9781574882902</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 4940103</span></nobr>

</td>
<td>John Adams Wickham</td>
<td>Brassey's; Potomac Books Inc.</td>
<td><nobr>2000</nobr></td>
<td>English</td>
<td>52</td>
<td><nobr><a href="/file.php?id=102463349">823 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=cfdcdf024f2dc8401d1d2d4e62fe1e16"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/cfdcdf024f2dc8401d1d2d4e62fe1e16"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/cfdcdf024f2dc8401d1d2d4e62fe1e16?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/cfdcdf024f2dc8401d1d2d4e62fe1e16"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2023-09-27/2024-01-04; ID: 103801171<br>10.1515_9781400866243" href="edition.php?id=92120301">The Muslim Brotherhood: Evolution of an Islamist Movement - Updated Edition <i>Updated edition with a New afterword by the author</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2023-09-27/2024-01-04; ID: 103801171<br>10.1515_9781400866243" href="edition.php?id=92120301"><i><font color="green"> 9781400866243; 1400866243</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2023-09-27/2024-01-04; ID: 103801171<br>10.1515_9781400866243" href="edition.php?id=92120301"><i><font color="green">DOI: 10.1515/9781400866243</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Monograph">mon</a></span> 
<span class="badge badge-secondary"">l 5275849</span></nobr>

</td>
<td>Carrie Rosefsky Wickham; Carrie Rosefsky Wickham</td>
<td>Princeton University Press</td>
<td><nobr>2015 December 31</nobr></td>
<td>English</td>
<td>424 / 424</td>
<td><nobr><a href="/file.php?id=103801171">2 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=57c21702cf825453ae502164d7a87bbd"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/57c21702cf825453ae502164d7a87bbd"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/57c21702cf825453ae502164d7a87bbd?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/57c21702cf825453ae502164d7a87bbd"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115064306<br>Wickham M. ( Sophie Kinsella ) - Shopaholic 02. Shopaholik za hranicemi - Wickham M. (Sophie Kinsella)" href="edition.php?id=207711646">Shopaholic 02. Shopaholik za hranicemi - Wickham M. (Sophie Kinsella) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7695330</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115064306">320 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=7be9cf18083ecb4cc8fe6717ab6e70f6"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/7be9cf18083ecb4cc8fe6717ab6e70f6"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/7be9cf18083ecb4cc8fe6717ab6e70f6?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/7be9cf18083ecb4cc8fe6717ab6e70f6"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115064308<br>Wickham M. ( Sophie Kinsella ) - Shopaholic 04. Báječné nakupování se sestrou - Wickham M. (Sophie Kinsella)" href="edition.php?id=207711648">Shopaholic 04. Báječné nakupování se sestrou - Wickham M. (Sophie Kinsella) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7695332</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115064308">321 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=0e2aeb27e55cd5302d79424a6fc0ed11"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/0e2aeb27e55cd5302d79424a6fc0ed11"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/0e2aeb27e55cd5302d79424a6fc0ed11?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/0e2aeb27e55cd5302d79424a6fc0ed11"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115064309<br>Wickham M. ( Sophie Kinsella ) - Shopaholic 03. Báječné nakupování před svadbou - Wickham M. (Sophie Kinsella)" href="edition.php?id=207711649">Shopaholic 03. Báječné nakupování před svadbou - Wickham M. (Sophie Kinsella) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7695333</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115064309">337 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=b7ee6daca8b19f60d1faeb43f30cc478"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/b7ee6daca8b19f60d1faeb43f30cc478"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/b7ee6daca8b19f60d1faeb43f30cc478?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/b7ee6daca8b19f60d1faeb43f30cc478"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115064310<br>Wickham M. ( Sophie Kinsella ) - Shopaholic 06. Báječní mininakupování - Wickham M. (Sophie Kinsella)" href="edition.php?id=207711650">Shopaholic 06. Báječní mininakupování - Wickham M. (Sophie Kinsella) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7695334</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115064310">357 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=7920cfd72a9eeed198cc7a8eb7e6f1b8"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/7920cfd72a9eeed198cc7a8eb7e6f1b8"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/7920cfd72a9eeed198cc7a8eb7e6f1b8?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/7920cfd72a9eeed198cc7a8eb7e6f1b8"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115064311<br>Wickham M. ( Sophie Kinsella ) - Shopaholic 05. Báječné nakupování do kočárku - Wickham M. (Sophie Kinsella)" href="edition.php?id=207711651">Shopaholic 05. Báječné nakupování do kočárku - Wickham M. (Sophie Kinsella) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7695335</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115064311">347 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=af3ff134f1beb44d4b6ac4e9151c6832"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/af3ff134f1beb44d4b6ac4e9151c6832"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/af3ff134f1beb44d4b6ac4e9151c6832?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/af3ff134f1beb44d4b6ac4e9151c6832"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115075504<br>Wickham M. ( Sophie Kinsella ) - Nezvaný host - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207722844">Nezvaný host - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7698709</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115075504">283 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=804aae603a66618858b20a24d5d4ea24"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/804aae603a66618858b20a24d5d4ea24"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/804aae603a66618858b20a24d5d4ea24?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/804aae603a66618858b20a24d5d4ea24"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115077592<br>Wickham M. ( Sophie Kinsella ) - Dokonalá nevěsta - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207724933">Dokonalá nevěsta - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7699060</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115077592">250 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=bd7b85b0560851edb96a6b32f12efcc8"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/bd7b85b0560851edb96a6b32f12efcc8"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/bd7b85b0560851edb96a6b32f12efcc8?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/bd7b85b0560851edb96a6b32f12efcc8"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115077605<br>Wickham M. ( Sophie Kinsella ) - Dokážete udržet tajemství - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207724946">Dokážete udržet tajemství - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7699069</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115077605">299 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=7b6f2eb3e47596596b4088ff290e5147"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/7b6f2eb3e47596596b4088ff290e5147"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/7b6f2eb3e47596596b4088ff290e5147?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/7b6f2eb3e47596596b4088ff290e5147"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115078341<br>Wickham M. ( Sophie Kinsella ) - V rytmu charlestonu - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207725682">V rytmu charlestonu - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7699344</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115078341">385 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=f84d99d47f2e6a0237b38b328d044110"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/f84d99d47f2e6a0237b38b328d044110"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/f84d99d47f2e6a0237b38b328d044110?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/f84d99d47f2e6a0237b38b328d044110"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115081372<br>Wickham M. ( Sophie Kinsella ) - Vzpomínáš si - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207728713">Vzpomínáš si - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7700073</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115081372">317 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=a12d93fbf8cd8aa883f83e75e3522b79"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/a12d93fbf8cd8aa883f83e75e3522b79"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/a12d93fbf8cd8aa883f83e75e3522b79?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/a12d93fbf8cd8aa883f83e75e3522b79"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2026-01-18/2026-01-18; ID: 115100487<br>Wickham M. ( Sophie Kinsella ) - Bohyně v domácnosti - Wickham M. ( Sophie Kinsella )" href="edition.php?id=207747827">Bohyně v domácnosti - Wickham M. ( Sophie Kinsella ) <i></i></a> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 7706741</span></nobr>

</td>
<td>Wickham M. ( Sophie Kinsella )</td>
<td></td>
<td><nobr></nobr></td>
<td>Czech</td>
<td>0</td>
<td><nobr><a href="/file.php?id=115100487">349 kB</a></nobr></td>
<td>epub</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=de096c2f3c2ce555c6ff64d12689ed65"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/de096c2f3c2ce555c6ff64d12689ed65"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/de096c2f3c2ce555c6ff64d12689ed65?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/de096c2f3c2ce555c6ff64d12689ed65"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b><a href="series.php?id=223754">Use R!   </a><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-07-15/2021-10-20; ID: 28133799<br>" href="edition.php?id=136580153"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-07-15/2021-10-20; ID: 28133799<br>" href="edition.php?id=136580153">ggplot2: Elegant Graphics for Data Analysis   <i>1</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-07-15/2021-10-20; ID: 28133799<br>" href="edition.php?id=136580153"><i><font color="green"> 0387981403; 9780387981406; 0387981411; 9780387981413</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-07-15/2021-10-20; ID: 28133799<br>" href="edition.php?id=136580153"><i><font color="green">DOI: 10.1007/978-0-387-98141-3</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 3147711</span> <span class="badge badge-secondary"">a 21577960</span></nobr>

</td>
<td>Hadley Wickham (auth.)</td>
<td>Springer</td>
<td><nobr>2009</nobr></td>
<td>English</td>
<td>0 / 213</td>
<td><nobr><a href="/file.php?id=28133799">9 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=abd8dcc405ec12871bbaa5848db42c8b"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/abd8dcc405ec12871bbaa5848db42c8b"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/abd8dcc405ec12871bbaa5848db42c8b?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/abd8dcc405ec12871bbaa5848db42c8b"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><b><a href="series.php?id=222584">Sociology Transformed   </a><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-08-26/2021-10-20; ID: 51552499<br>" href="edition.php?id=137257475"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-08-26/2021-10-20; ID: 51552499<br>" href="edition.php?id=137257475">Australian Sociology: Fragility, Survival, Rivalry <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-08-26/2021-10-20; ID: 51552499<br>" href="edition.php?id=137257475"><i><font color="green"> 9781349478941; 1349478946; 9781137379757; 1137379758</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2015-08-26/2021-10-20; ID: 51552499<br>" href="edition.php?id=137257475"><i><font color="green">DOI: 10.1057/9781137379757</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 3182317</span> <span class="badge badge-secondary"">a 45314170</span></nobr>

</td>
<td>Kirsten Harley, Gary Wickham (auth.)</td>
<td>Palgrave Pivot</td>
<td><nobr>2014</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=51552499">4 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=51ed733946fa01af17b1d28d3ce20a54"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/51ed733946fa01af17b1d28d3ce20a54"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/51ed733946fa01af17b1d28d3ce20a54?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/51ed733946fa01af17b1d28d3ce20a54"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-01-15/2021-10-21; ID: 55170347<br>" href="edition.php?id=137259068">Style and Form in the Hollywood Slasher Film <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-01-15/2021-10-21; ID: 55170347<br>" href="edition.php?id=137259068"><i><font color="green"> 9781349573455; 1349573450; 9781137496478; 1137496479</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-01-15/2021-10-21; ID: 55170347<br>" href="edition.php?id=137259068"><i><font color="green">DOI: 10.1057/9781137496478</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 3184064</span> <span class="badge badge-secondary"">a 48986734</span></nobr>

</td>
<td>Wickham Clayton (eds.)</td>
<td>Palgrave Macmillan</td>
<td><nobr>2015</nobr></td>
<td>English</td>
<td>0</td>
<td><nobr><a href="/file.php?id=55170347">1 MB</a></nobr></td>
<td>pdf</td>
<td><nobr><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=e3b70329c4af8b020f8e16b96f7dfc2e"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/e3b70329c4af8b020f8e16b96f7dfc2e"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/e3b70329c4af8b020f8e16b96f7dfc2e?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/e3b70329c4af8b020f8e16b96f7dfc2e"><span class="badge badge-primary">4</span></a> </nobr></td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2021-10-08; ID: 56000218<br>10.1057%2F9780230373679" href="edition.php?id=137250520">Economic Strategy and the Labour Party: Politics and policy-making, 1970–83 <i>1</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2021-10-08; ID: 56000218<br>10.1057%2F9780230373679" href="edition.php?id=137250520"><i><font color="green"> 9780333693728; 0333693728; 9780230373679; 0230373674; 9780312164058; 031216405X</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2021-10-08; ID: 56000218<br>10.1057%2F9780230373679" href="edition.php?id=137250520"><i><font color="green">DOI: 10.1057/9780230373679</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1473253</span> <span class="badge badge-secondary"">a 49817784</span></nobr>

</td>
<td>Mark Wickham-Jones (auth.)</td>
<td>Palgrave Macmillan</td>
<td><nobr>1996</nobr></td>
<td>English</td>
<td>304 / IX, 294</td>
<td><nobr><a href="/file.php?id=56000218">16 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=b643e2696d00a0f5d27ce0e61938d7f7"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/b643e2696d00a0f5d27ce0e61938d7f7"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/b643e2696d00a0f5d27ce0e61938d7f7?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/b643e2696d00a0f5d27ce0e61938d7f7"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/b643e2696d00a0f5d27ce0e61938d7f7"><span class="badge badge-primary">5</span></a> </td>
</tr><tr>

<td><b>Vigiliae Christianae, Supplements 19<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=58151820"><i> 1993-jan 01</i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=58151820">Christian Faith and Greek Philosophy in Late Antiquity <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=58151820"><i><font color="green">DOI: 10.1163/9789004312852</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2141951</span> <span class="badge badge-secondary"">a 51893805</span></nobr>

</td>
<td>Wickham, Lionel R. (editor);Bammel, Caroline P. (editor)</td>
<td>Brill Academic Publishers</td>
<td><nobr>1993 January 01</nobr></td>
<td></td>
<td>279</td>
<td><nobr><a href="/file.php?id=58062507">20 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/618f1ed7dc67a7cb7d189372d1c147d9?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">4</span></a> </td>
</tr><tr>

<td><b>Vigiliae Christianae, Supplements 19<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=137919218"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=137919218">Christian Faith and Greek Philosophy in Late Antiquity: Essays in Tribute to Christopher George Stead in Celebration of His Eightieth Birthday 9th April 1993 <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 58062507<br>10.1163@9789004312852" href="edition.php?id=137919218"><i><font color="green"> 9004096051; 9789004096059</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2141951</span> <span class="badge badge-secondary"">a 51893805</span></nobr>

</td>
<td>Lionel R Wickham, Caroline P Bammel, Dr Erica C D Hunter</td>
<td>Brill Academic Publishers</td>
<td><nobr>1993</nobr></td>
<td>English</td>
<td>279 / 266</td>
<td><nobr><a href="/file.php?id=58062507">20 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/618f1ed7dc67a7cb7d189372d1c147d9?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/618f1ed7dc67a7cb7d189372d1c147d9"><span class="badge badge-primary">4</span></a> </td>
</tr><tr>

<td><b><a href="series.php?id=223754">Use R!   </a><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2022-03-09; ID: 60863200<br>10.1007%2F978-3-319-24277-4" href="edition.php?id=137309817"><i></i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2022-03-09; ID: 60863200<br>10.1007%2F978-3-319-24277-4" href="edition.php?id=137309817">ggplot2: Elegant Graphics for Data Analysis <i>2nd Edition</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2022-03-09; ID: 60863200<br>10.1007%2F978-3-319-24277-4" href="edition.php?id=137309817"><i><font color="green"> 9783319242750; 331924275X; 9783319242774; 3319242776</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2022-03-09; ID: 60863200<br>10.1007%2F978-3-319-24277-4" href="edition.php?id=137309817"><i><font color="green">DOI: 10.1007/978-3-319-24277-4</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 1532550</span> <span class="badge badge-secondary"">a 54741939</span></nobr>

</td>
<td>Sievert, Carson;Wickham, Hadley(auth.)</td>
<td>Springer International Publishing</td>
<td><nobr>2016</nobr></td>
<td>English</td>
<td>268 / XVI, 260</td>
<td><nobr><a href="/file.php?id=60863200">9 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=b5ab6480fbc1917491eb746aac2c65d7"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/b5ab6480fbc1917491eb746aac2c65d7"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/b5ab6480fbc1917491eb746aac2c65d7?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/b5ab6480fbc1917491eb746aac2c65d7"><span class="badge badge-primary">4</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="bookfi.net" href="http://bookfi.net/md5/b5ab6480fbc1917491eb746aac2c65d7"><span class="badge badge-primary">5</span></a> </td>
</tr><tr>

<td><b>Translated Texts for Historians 25<a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-10-25/2022-03-09; ID: 68163437<br>" href="edition.php?id=68411519"><i> 1997-jan</i></a></b><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-10-25/2022-03-09; ID: 68163437<br>" href="edition.php?id=68411519">Hilary of Poitiers: conflicts of conscience and law in the fourth-century Church: Against Valens and Ursacius: the extant fragments, together with his Letter to the Emperor Constantius <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-10-25/2022-03-09; ID: 68163437<br>" href="edition.php?id=68411519"><i><font color="green"> 0853235724; 9780853235729</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2016-10-25/2022-03-09; ID: 68163437<br>" href="edition.php?id=68411519"><i><font color="green">DOI: 10.3828/978-0-85323-572-9</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Monograph">mon</a></span> 
<span class="badge badge-secondary"">a 62153547</span></nobr>

</td>
<td>Hilaire;Wickham, Lionel R</td>
<td>Liverpool University Press</td>
<td><nobr>1997 January</nobr></td>
<td></td>
<td>0</td>
<td><nobr><a href="/file.php?id=68163437">18 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=a9e56bf8b1730789ed52e6ac6550d30a&downloadname=10.3828/978-0-85323-572-9"><span class="badge badge-primary">Libgen</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="sci-hub" href="http://sci-hub.ru/10.3828/978-0-85323-572-9"><span class="badge badge-primary">Sci-Hub</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/a9e56bf8b1730789ed52e6ac6550d30a"><span class="badge badge-primary">Randombook</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/a9e56bf8b1730789ed52e6ac6550d30a"><span class="badge badge-primary">libgen.pw</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/a9e56bf8b1730789ed52e6ac6550d30a?r=Ax2w6jC"><span class="badge badge-primary">Anna's arch</span></a> </td>
</tr><tr>

<td><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 73429585<br>10.1007%2F978-1-4842-3333-7" href="edition.php?id=137956259"> Practical Android: 14 Complete Projects on Advanced Techniques and Approaches <i>1</i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 73429585<br>10.1007%2F978-1-4842-3333-7" href="edition.php?id=137956259"><i><font color="green"> 9781484233320; 1484233328; 9781484233337; 1484233336</font></a></i><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-09-01/2024-12-16; ID: 73429585<br>10.1007%2F978-1-4842-3333-7" href="edition.php?id=137956259"><i><font color="green">DOI: 10.1007/978-1-4842-3333-7</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">l 2178992</span> <span class="badge badge-secondary"">a 67513854</span></nobr>

</td>
<td>Mark Wickham (auth.)</td>
<td>Apress</td>
<td><nobr>2018</nobr></td>
<td>English</td>
<td>253 / XXIX, 228</td>
<td><nobr><a href="/file.php?id=73429585">5 MB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=cdb80d623ba3f080724f852d0dfa71aa"><span class="badge badge-primary">1</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/cdb80d623ba3f080724f852d0dfa71aa"><span class="badge badge-primary">2</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/cdb80d623ba3f080724f852d0dfa71aa?r=Ax2w6jC"><span class="badge badge-primary">3</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/cdb80d623ba3f080724f852d0dfa71aa"><span class="badge badge-primary">4</span></a> </td>
</tr><tr>

<td><b>Oxford Handbooks Online</b><p><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-08-06/2021-07-21; ID: 77214636<br>" href="edition.php?id=77595298">Coastal Adaptations <i></i></a><br><a data-toggle="tooltip" data-placement="right" data-html="true" title="Add/Edit : 2018-08-06/2021-07-21; ID: 77214636<br>" href="edition.php?id=77595298"><i><font color="green">DOI: 10.1093/oxfordhb/9780199551224.013.009</font></a></i> 
<nobr><span class="badge badge-primary"><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Book">b</a></span> 
<span class="badge badge-secondary"">a 71346902</span></nobr>

</td>
<td>Wickham-Jones, C.R. (author)</td>
<td>Oxford University Press</td>
<td><nobr>2013 October 01</nobr></td>
<td></td>
<td>0</td>
<td><nobr><a href="/file.php?id=77214636">232 kB</a></nobr></td>
<td>pdf</td>
<td><a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen" href="/ads.php?md5=80a1879247f544ab624389fea52fd1e0&downloadname=10.1093/oxfordhb/9780199551224.013.009"><span class="badge badge-primary">Libgen</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="sci-hub" href="http://sci-hub.ru/10.1093/oxfordhb/9780199551224.013.009"><span class="badge badge-primary">Sci-Hub</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="Randombook" href="https://randombook.org/book/80a1879247f544ab624389fea52fd1e0"><span class="badge badge-primary">Randombook</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="libgen.pw" href="https://libgen.pw/book/80a1879247f544ab624389fea52fd1e0"><span class="badge badge-primary">libgen.pw</span></a> <a data-toggle="tooltip" data-placement="bottom" data-html="true" title="anna's archive" href="https://en.annas-archive.gl/md5/80a1879247f544ab624389fea52fd1e0?r=Ax2w6jC"><span class="badge badge-primary">Anna's arch</span></a> </td>
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
</table><div style="text-align: center;" class="paginator" id="paginator_example_bottom"></div><script type="text/javascript">paginator_example_bottom = new Paginator("paginator_example_bottom", 14, 25, 1, "/index.php?req=Wickham&columns%5B%5D=a&objects%5B%5D=e&objects%5B%5D=f&objects%5B%5D=a&topics%5B%5D=l&res=25&curtab=f&order=&ordermode=desc&filesuns=all&page=" );</script><div class="modal fade text-dark" id="googlemodemodal" tabindex="-1" aria-labelledby="googlemodemodalLabel" aria-hidden="true">
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
	<span class="navbar-text">Users online 6078</span>
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