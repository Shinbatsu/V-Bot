CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Users table
CREATE TABLE IF NOT EXISTS `users` (
  `id` INTEGER PRIMARY KEY,
  `activity` INTEGER NOT NULL DEFAULT 0,
  `boosts_count` INTEGER NOT NULL DEFAULT 0,
  `valorant_nickname` VARCHAR(255) DEFAULT NULL,
  `valorant_rank` VARCHAR(255) DEFAULT NULL,
  `send_notifications` BOOLEAN NOT NULL DEFAULT 0,
  `messages_count` INTEGER NOT NULL DEFAULT 0
);

-- UserRooms table
CREATE TABLE IF NOT EXISTS `user_rooms` (
  `id` INTEGER PRIMARY KEY,
  `user_id` INTEGER,
  `room_id` INTEGER NOT NULL,
  `room_name` VARCHAR(255) NOT NULL,
  `is_closed` BOOLEAN NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (`room_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);
-- BlockedUsers table
CREATE TABLE IF NOT EXISTS `blocked_users` (
  `id` INTEGER PRIMARY KEY,
  `user_id` INTEGER,
  `blocked_user_id` INTEGER,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`blocked_user_id`) REFERENCES `users`(`id`)
);
-- UserReports table
CREATE TABLE IF NOT EXISTS `user_reports` (
  `id` INTEGER PRIMARY KEY,
  `user_id` INTEGER,
  `reported_user_id` INTEGER,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  FOREIGN KEY (`reported_user_id`) REFERENCES `users`(`id`)
);