<?php
global $pdo;
include 'db.php';

$data = json_decode(file_get_contents("php://input"), true);

$guest_name = $data['guest_name'];
$phone_number = $data['phone_number'];
$email = $data['email'];
$room_id = $data['room_id'];
$check_in_date = $data['check_in_date'];
$check_out_date = $data['check_out_date'];

try {
    $guest_query = $pdo->prepare("SELECT guest_id FROM Guest WHERE phone_number = ? OR email = ?");
    $guest_query->execute([$phone_number, $email]);
    $guest = $guest_query->fetch(PDO::FETCH_ASSOC);

    if (!$guest) {
        $insert_guest = $pdo->prepare("INSERT INTO Guest (guest_name, phone_number, email) VALUES (?, ?, ?)");
        $insert_guest->execute([$guest_name, $phone_number, $email]);
        $guest_id = $pdo->lastInsertId();
    } else {
        $guest_id = $guest['guest_id'];
    }

    $insert_booking = $pdo->prepare("
        INSERT INTO Booking (guest_id, room_id, check_in_date, check_out_date) 
        VALUES (?, ?, ?, ?)
    ");
    $insert_booking->execute([$guest_id, $room_id, $check_in_date, $check_out_date]);

    $update_room = $pdo->prepare("UPDATE Room SET status = 'Occupied' WHERE room_id = ?");
    $update_room->execute([$room_id]);

    echo json_encode(["message" => "Room successfully booked!"]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => $e->getMessage()]);
}
?>

