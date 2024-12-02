<?php
global $pdo;
include 'db.php';

$query = $pdo->query("
    SELECT 
        room_id,
        room_type,
        price,
        room_condition,
        status,
        room_view,
        amenities
    FROM Room
");
$rooms = $query->fetchAll(PDO::FETCH_ASSOC);

header('Content-Type: application/json');
echo json_encode($rooms);
?>
