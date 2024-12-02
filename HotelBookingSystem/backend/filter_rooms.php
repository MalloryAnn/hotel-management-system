<?php
global $pdo;
include 'db.php';

try {
    $start_date = filter_input(INPUT_GET, 'start_date', FILTER_SANITIZE_STRING);
    $end_date = filter_input(INPUT_GET, 'end_date', FILTER_SANITIZE_STRING);

    $query = $pdo->prepare("
        SELECT Room.room_id, room_type, price, room_condition, status
        FROM Room
        LEFT JOIN Booking 
        ON Room.room_id = Booking.room_id
        AND NOT (Booking.check_out_date < :start_date OR Booking.check_in_date > :end_date)
        WHERE Booking.room_id IS NULL AND Room.status = 'Vacant'
    ");
    $query->execute(['start_date' => $start_date, 'end_date' => $end_date]);
    $rooms = $query->fetchAll(PDO::FETCH_ASSOC);

    header('Content-Type: application/json');
    echo json_encode($rooms);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to filter rooms', 'details' => $e->getMessage()]);
}
?>
