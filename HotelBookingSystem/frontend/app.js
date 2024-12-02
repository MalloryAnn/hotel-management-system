function fetchAvailableRooms(startDate, endDate) {
    fetch(`backend/filter_rooms.php?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(rooms => {
            const roomList = document.getElementById('room-list');
            roomList.innerHTML = ''; // Clear previous results

            rooms.forEach(room => {
                const roomDiv = document.createElement('div');
                roomDiv.textContent = `Room ${room.room_id}: ${room.room_type} - $${room.price}`;
                roomList.appendChild(roomDiv);
            });
        });
}
