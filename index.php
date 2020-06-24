<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Парсер новостей</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <style>
            body {
                font-family: 'Arial';
            }
            a {
                color: black;
            }
            .pd {
                margin: 10px;
            }
            .z {
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div>
            <center>
                <br>
                <h1>Просмотр содержимого базы данных</h1>
                <br>
                <h2>Нажмите на кнопку для просмотра содержимого таблицы</h2>
                <br>
                <?php header("Content-Type: text/html; charset=utf-8"); ?>
                <?php
                    $db = new SQLite3('parser.db');
                    $results_ria = $db->query('SELECT * FROM ria');
                    $results_iz = $db->query('SELECT * FROM iz');
                    $results_bbc = $db->query('SELECT * FROM bbc');
                    $results_rt = $db->query('SELECT * FROM rt');
                    $results_vesti = $db->query('SELECT * FROM vesti');
                    $results_rosatom = $db->query('SELECT * FROM rosatom');
                    $results_tvel = $db->query('SELECT * FROM tvel');
                    $results_rbk = $db->query('SELECT * FROM rbk');
                    $results_komm = $db->query('SELECT * FROM komm');
                    
                    echo '<button class="btn btn-info"><h2 onclick="rhide(rria)">Новости из источника РИА</h2></button>';
                    echo "<div id='rria' style='display: none'>";
                    
                    while ($row = $results_ria->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                        
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(riz)">Новости из источника Известия</h2></button>';
                    echo "<div id='riz' style='display: none'>";
                
                    while ($row = $results_iz->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                    
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rbbc)">Новости из источника BBC</h2></button>';
                    echo "<div id='rbbc' style='display: none'>";  
                
                    while ($row = $results_bbc->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                    
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rrt)">Новости из источника RussiaToday</h2></button>';
                    echo "<div id='rrt' style='display: none'>";    
                
                    while ($row = $results_rt->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                        
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rvesti)">Новости из источника Вести</h2></button>';
                    echo "<div id='rvesti' style='display: none'>";
                
                    while ($row = $results_vesti->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";

                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rrosatom)">Новости из источника Росатом</h2></button>';
                    echo "<div id='rrosatom' style='display: none'>";
                
                    while ($row = $results_rosatom->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                        
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rtvel)">Новости из источника ТВЭЛ</h2></button>';
                    echo "<div id='rtvel' style='display: none'>";
                
                    while ($row = $results_tvel->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                    
                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rrbk)">Новости из источника РБК</h2></button>';                   
                    echo "<div id='rrbk' style='display: none'>"; 
                
                    while ($row = $results_rbk->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";

                    echo '<br><br><button class="btn btn-info"><h2 onclick="rhide(rkomm)">Новости из источника Коммерсантъ</h2></button>';                
                    echo "<div id='rkomm' style='display: none'>";    
                
                    while ($row = $results_komm->fetchArray()) {
                        echo "<div style='border: 2px dotted #17a2b8; margin-top: 15px;' class='col-md-10 z col-xs-12 col-sm-12'>";
                        echo "<a href='$row[1]' class='pd'><h4>$row[0] | $row[2]</h4></a>";
                        echo "</div>";}
                    echo "</div>";
                ?>
            </center>
        </div>
        <script>
        rria = document.getElementById("rria")
        riz = document.getElementById("riz")
        rbbc = document.getElementById("rbbc")
        rrt = document.getElementById("rrt")
        rvesti = document.getElementById("rvesti")
        rrosatom = document.getElementById("rrosatom")
        rtvel = document.getElementById("rtvel")
        rrbk = document.getElementById("rrbk")
        rkomm = document.getElementById("rkomm")
        function rhide(elem) {
            elem.style.display = (elem.style.display == "none") ? "" : "none"
        }
        </script>
    </body>
</html>