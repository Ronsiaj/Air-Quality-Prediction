<?php
session_start();
include("dbconnect.php");
extract($_REQUEST);

$q1=mysqli_query($connect,"select * from air_location");
		$r1=mysqli_fetch_array($q1);
		/*$lat1=$r1['latitude'];
		$q11=mysql_query("select * from crime_data where district like '%$dest1%'");
		$r11=mysql_fetch_array($q11);
		$lat2=$r11['latitude'];
		
		if($lat1>$lat2)
		{
		$d1=$lat2;
		$d2=$lat1;
		}
		else
		{
		$d1=$lat1;
		$d2=$lat2;
		}
		
		
			$sq1=mysql_query("select district,latitude,longitude,sum(crime1),sum(crime2),sum(crime3),sum(crime4),sum(crime5),sum(crime6) from crime_data where latitude between $d1 and $d2 group by district");
			
			$sq11=mysql_query("select district,latitude,longitude,sum(crime1),sum(crime2),sum(crime3),sum(crime4),sum(crime5),sum(crime6) from crime_data where latitude between $d1 and $d2 group by district");*/
?>
<html>
<head>
  
  <title>Google Maps Multiple Markers</title>
  <script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>
</head>
<body>

  <div id="map" style="height: 800px; width: 800px;">
</div>
<script type="text/javascript">
    var locations = [
		<?php
		/*while($sr1=mysql_fetch_array($sq1))
		{
		$s1=$sr1['sum(crime1)']+$sr1['sum(crime2)']+$sr1['sum(crime3)']+$sr1['sum(crime4)']+$sr1['sum(crime5)']+$sr1['sum(crime6)'];
			if($s1>1500)
			{
		?>
      ['<?php echo $sr1['district']; ?>, UNSAFE', <?php echo $sr1['latitude']; ?>, <?php echo $sr1['longitude']; ?>, 4],
	  	<?php
			}
			
		}*/
		?>
		
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Good'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Chennai', 13.084622, 80.248357, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	
	/////////////////////////////////////////////////////////////////
	var locations2 = [
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Satisfactory'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Coogee Beach', 11.005547, 76.966122, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	/////////////////////////////////////////////////////////////////
	var locations3 = [
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Moderate'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Coogee Beach', 11.005547, 76.966122, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	
	/////////////////////////////////////////////////////////////////
	var locations4 = [
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Poor'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Coogee Beach', 11.005547, 76.966122, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	/////////////////////////////////////////////////////////////////
	var locations5 = [
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Very Poor'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Coogee Beach', 11.005547, 76.966122, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	/////////////////////////////////////////////////////////////////
	var locations6 = [
		<?php
		###
		$q4=mysqli_query($connect,"select * from air_location where aqi_bucket='Severe'");
		while($r4=mysqli_fetch_array($q4))
		{
		
		?>
      ['<?php echo $r4['city']; ?>', <?php echo $r4['lat']; ?>, <?php echo $r4['lon']; ?>, 2],
	  	<?php
		}
		?>
      /*['Coogee Beach', 11.005547, 76.966122, 5],
      ['Cronulla Beach', -34.028249, 151.157507, 3],
      ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
      ['Maroubra Beach', -33.950198, 151.259302, 1]*/
    ];
	
	
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 10,
      center: new google.maps.LatLng(10.790483, 78.704673),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;
	////////////////////////////////
    for (i = 0; i < locations.length; i++) { 
	
	var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#009933'
    });
	
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
	///////////////////////////////////////////
	 for (i = 0; i < locations2.length; i++) { 
	 
	 var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#00CC99'
    });
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations2[i][1], locations2[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations2[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
///////////////////////////////////////////
	 for (i = 0; i < locations3.length; i++) { 
	 
	 var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#0000FF'
    });
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations3[i][1], locations3[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations3[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
///////////////////////////////////////////
	 for (i = 0; i < locations4.length; i++) { 
	 
	 var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#FF6600'
    });
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations4[i][1], locations4[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations4[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
///////////////////////////////////////////
	 for (i = 0; i < locations5.length; i++) { 
	 
	 var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#FFFF00'
    });
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations5[i][1], locations5[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/orange-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations5[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
///////////////////////////////////////////
	 for (i = 0; i < locations6.length; i++) { 
	 
	 var circle = new google.maps.Circle({
      map: map,
      radius: 1000,
      fillColor: '#FF0000'
    });
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations6[i][1], locations6[i][2]),
        map: map
      });
marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
circle.bindTo('center', marker, 'position');

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations6[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
					
	
//////////////////////////////////////	
	
	
  </script> 
<a href="search.php">Back</a>
</body>
</html>
