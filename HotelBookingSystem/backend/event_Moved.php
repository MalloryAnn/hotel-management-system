<?php
global $pdo;
include 'db.php';

try {
    $data = json_decode(file_get_contents("php://input"), true);

    $id = filter_var($data['id'], FILTER_SANITIZE_NUMBER_INT);
    $start_date = $data['start'];
    $end_date = $data['end'];

    $query = $pdo->prepare("UPDATE bookings SET start_date = ?, end_date = ? WHERE id = ?");
    $query->execute([$start_date, $end_date, $id]);

    header('Content-Type: application/json');
    echo json_encode(["status" => "success", "message" => "Booking updated successfully!"]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
?>

