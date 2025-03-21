-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               9.2.0 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table threads_db.accounts_myuser: ~2 rows (approximately)
INSERT INTO `accounts_myuser` (`id`, `bio`, `profile_picture`, `user_id`, `link`) VALUES
	(1, NULL, '', 1, NULL),
	(2, NULL, '', 2, 'Test avatar'),
	(3, 'New bio text', '', 3, 'new_avatar_link'),
	(8, NULL, '', 6, NULL),
	(12, NULL, '', 8, NULL),
	(13, NULL, '', 9, NULL),
	(16, NULL, '', 11, NULL),
	(18, NULL, '', 12, NULL),
	(20, NULL, '', 13, NULL),
	(22, NULL, '', 14, NULL),
	(23, NULL, '', 15, NULL),
	(24, NULL, '', 16, NULL),
	(25, NULL, '', 17, NULL),
	(26, NULL, '', 18, NULL),
	(27, NULL, '', 19, NULL),
	(29, NULL, '', 20, NULL),
	(30, NULL, '', 21, NULL);

-- Dumping data for table threads_db.auth_group: ~0 rows (approximately)

-- Dumping data for table threads_db.auth_group_permissions: ~0 rows (approximately)

-- Dumping data for table threads_db.auth_permission: ~72 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add thread', 1, 'add_thread'),
	(2, 'Can change thread', 1, 'change_thread'),
	(3, 'Can delete thread', 1, 'delete_thread'),
	(4, 'Can view thread', 1, 'view_thread'),
	(5, 'Can add like', 2, 'add_like'),
	(6, 'Can change like', 2, 'change_like'),
	(7, 'Can delete like', 2, 'delete_like'),
	(8, 'Can view like', 2, 'view_like'),
	(9, 'Can add follow', 3, 'add_follow'),
	(10, 'Can change follow', 3, 'change_follow'),
	(11, 'Can delete follow', 3, 'delete_follow'),
	(12, 'Can view follow', 3, 'view_follow'),
	(13, 'Can add comment', 4, 'add_comment'),
	(14, 'Can change comment', 4, 'change_comment'),
	(15, 'Can delete comment', 4, 'delete_comment'),
	(16, 'Can view comment', 4, 'view_comment'),
	(17, 'Can add repost', 5, 'add_repost'),
	(18, 'Can change repost', 5, 'change_repost'),
	(19, 'Can delete repost', 5, 'delete_repost'),
	(20, 'Can view repost', 5, 'view_repost'),
	(21, 'Can add thread image', 6, 'add_threadimage'),
	(22, 'Can change thread image', 6, 'change_threadimage'),
	(23, 'Can delete thread image', 6, 'delete_threadimage'),
	(24, 'Can view thread image', 6, 'view_threadimage'),
	(25, 'Can add comment image', 7, 'add_commentimage'),
	(26, 'Can change comment image', 7, 'change_commentimage'),
	(27, 'Can delete comment image', 7, 'delete_commentimage'),
	(28, 'Can view comment image', 7, 'view_commentimage'),
	(29, 'Can add like comment', 8, 'add_likecomment'),
	(30, 'Can change like comment', 8, 'change_likecomment'),
	(31, 'Can delete like comment', 8, 'delete_likecomment'),
	(32, 'Can view like comment', 8, 'view_likecomment'),
	(33, 'Can add repost comment', 9, 'add_repostcomment'),
	(34, 'Can change repost comment', 9, 'change_repostcomment'),
	(35, 'Can delete repost comment', 9, 'delete_repostcomment'),
	(36, 'Can view repost comment', 9, 'view_repostcomment'),
	(37, 'Can add notification', 10, 'add_notification'),
	(38, 'Can change notification', 10, 'change_notification'),
	(39, 'Can delete notification', 10, 'delete_notification'),
	(40, 'Can view notification', 10, 'view_notification'),
	(41, 'Can add my user', 11, 'add_myuser'),
	(42, 'Can change my user', 11, 'change_myuser'),
	(43, 'Can delete my user', 11, 'delete_myuser'),
	(44, 'Can view my user', 11, 'view_myuser'),
	(45, 'Can add log entry', 12, 'add_logentry'),
	(46, 'Can change log entry', 12, 'change_logentry'),
	(47, 'Can delete log entry', 12, 'delete_logentry'),
	(48, 'Can view log entry', 12, 'view_logentry'),
	(49, 'Can add permission', 13, 'add_permission'),
	(50, 'Can change permission', 13, 'change_permission'),
	(51, 'Can delete permission', 13, 'delete_permission'),
	(52, 'Can view permission', 13, 'view_permission'),
	(53, 'Can add group', 14, 'add_group'),
	(54, 'Can change group', 14, 'change_group'),
	(55, 'Can delete group', 14, 'delete_group'),
	(56, 'Can view group', 14, 'view_group'),
	(57, 'Can add user', 15, 'add_user'),
	(58, 'Can change user', 15, 'change_user'),
	(59, 'Can delete user', 15, 'delete_user'),
	(60, 'Can view user', 15, 'view_user'),
	(61, 'Can add content type', 16, 'add_contenttype'),
	(62, 'Can change content type', 16, 'change_contenttype'),
	(63, 'Can delete content type', 16, 'delete_contenttype'),
	(64, 'Can view content type', 16, 'view_contenttype'),
	(65, 'Can add session', 17, 'add_session'),
	(66, 'Can change session', 17, 'change_session'),
	(67, 'Can delete session', 17, 'delete_session'),
	(68, 'Can view session', 17, 'view_session'),
	(69, 'Can add kv store', 18, 'add_kvstore'),
	(70, 'Can change kv store', 18, 'change_kvstore'),
	(71, 'Can delete kv store', 18, 'delete_kvstore'),
	(72, 'Can view kv store', 18, 'view_kvstore'),
	(73, 'Can add profile', 19, 'add_profile'),
	(74, 'Can change profile', 19, 'change_profile'),
	(75, 'Can delete profile', 19, 'delete_profile'),
	(76, 'Can view profile', 19, 'view_profile');

-- Dumping data for table threads_db.auth_user: ~3 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$600000$ORBc90SZH9b8qSMrotViSp$fM4gfx23yH7MhCmSj2xHhEcCOelQ7gq76XOTEc2wwWQ=', '2025-03-19 14:35:33.772342', 0, 'testuser', '', '', 'test@example.com', 0, 1, '2025-03-19 14:04:01.195295'),
	(2, 'pbkdf2_sha256$600000$BJw0KG1VJ1awX1eqsHFOu6$BxT5WNHpvw8WzXPeYMhjKoeZ3zRw0RUE7UEjoWvSXaM=', '2025-03-20 12:04:08.259675', 0, 'testuser2', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-19 15:54:54.388729'),
	(3, 'pbkdf2_sha256$600000$OI2VSriq1MBL66ltoYOhAN$66KGlbENh46+sa8pu1W3sFyqVRqZZH8IKgbass5BbFQ=', '2025-03-20 08:43:12.706437', 0, 'newuser', 'New John', 'New Da', 'new.email@example.com', 0, 1, '2025-03-20 08:42:42.216646'),
	(6, 'pbkdf2_sha256$600000$os8US858fmOhN9RZfgFHPT$OR4DWbfYTaP9HLsKbbJ0KRu1B7IUkzdd91vTDzjhUvg=', NULL, 0, 'npthanh24', 'Wing', '2K8', 'user@example.com', 0, 1, '2025-03-21 03:08:06.280881'),
	(8, 'pbkdf2_sha256$600000$Hx1TogcNsIUN9Rse5K4WZg$2lfp4ZliG4vO4tuPOpLMlVUuisGOJpcWBBFSbGjqvRM=', NULL, 0, 'npthanh2004', 'Wing', '2K8', 'user@example.com', 0, 1, '2025-03-21 03:10:30.948970'),
	(9, 'pbkdf2_sha256$600000$WWMLvJkJwg0dRpv7vR0AYP$tW45DMXrqQ5ErcXIE75U8TSmZ263+t3q/OoSrr+mRk4=', '2025-03-21 03:26:02.888337', 0, 'npthanhTest', 'Wing', '2K8', 'user@example.com', 0, 1, '2025-03-21 03:10:51.642620'),
	(11, 'pbkdf2_sha256$600000$YuOy6ShT9p1QancKDBtyh6$oAX7Qb0GzoqmSAGXlGg2ppL75PLA6qJVB5Jx4tN/4zM=', NULL, 0, 'newuser1', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:35:50.319210'),
	(12, 'pbkdf2_sha256$600000$e0CQ379ER1pR5yGXbutGuZ$pPi6l3/lAraVIUsKWy04QV1QiGKMCTLtZY+A4YKURI4=', NULL, 0, 'newuser2', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:37:57.432654'),
	(13, 'pbkdf2_sha256$600000$YelXcO8sGHehD34MjfQjBy$nxrIwcAm1dLCvbwEU3A1Khtv4Mx89h2v62qo2BgIhrg=', NULL, 0, 'newuse2', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:38:05.190803'),
	(14, 'pbkdf2_sha256$600000$7a18gnSWAIzC7wRt3OMqJ3$Vv6uoAo4BNaQuKO2m3czliZOv+XaX/w32CBAJEzDx7E=', NULL, 0, 'newuserthanh', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:38:48.841730'),
	(15, 'pbkdf2_sha256$600000$yoPa4688CR4lNUQlm0S4dW$rAdjqjIt2z2ua3mLiUH9tvHNyvwt4huKnARXyNUAvM8=', NULL, 0, 'newuserthanh1', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:39:01.693947'),
	(16, 'pbkdf2_sha256$600000$EG8L9YzYICw5OnfjdBjUZv$5i+NrBwakigPTxOHlej+JESs8UOEAzlf6SOlIsTAAaQ=', NULL, 0, 'newuserthanh2', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:39:12.653468'),
	(17, 'pbkdf2_sha256$600000$H8DIR5X1VdMhA1wiZ5RLP5$iAF4iL+wVM3ZwjqkzNb3noXugCZkz8PXDeNLzLCKY/0=', NULL, 0, 'newuserthanh5', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:39:56.220951'),
	(18, 'pbkdf2_sha256$600000$Mbzcj2nGzrxCq4NX20G2UC$zKjgwxV+BDV0RegN/r8MA3sAZAo/LvcobqaPrr+ACrc=', NULL, 0, 'newuserthanh4', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:40:36.117491'),
	(19, 'pbkdf2_sha256$600000$P2KxkCMSezOQh2K5LQGb2m$xyZsgDcF3LMjMWcOULf0VUQAWBnNU7MenKNqWevtyHk=', NULL, 0, 'newuserthanh3', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:41:55.018154'),
	(20, 'pbkdf2_sha256$600000$Nfmc9ehPrepmWHxV2pAYID$E47T0OIeuCd2rVIUEQOl0tS3ckUE8DFW1zkvBmoLGrU=', NULL, 0, 'newuserthanh6', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:42:46.748865'),
	(21, 'pbkdf2_sha256$600000$3h8v3WiURGuWA9w7viG3ii$L/z86cpwvdLiFne48t13xV6yit+6bj5N1pjrJTbUrPk=', '2025-03-21 03:43:53.342644', 0, 'newuserthanh7', 'John', 'Doe', 'user@example.com', 0, 1, '2025-03-21 03:42:52.191155');

-- Dumping data for table threads_db.auth_user_groups: ~0 rows (approximately)

-- Dumping data for table threads_db.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping data for table threads_db.django_admin_log: ~0 rows (approximately)

-- Dumping data for table threads_db.django_content_type: ~18 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(11, 'accounts', 'myuser'),
	(19, 'accounts', 'profile'),
	(12, 'admin', 'logentry'),
	(14, 'auth', 'group'),
	(13, 'auth', 'permission'),
	(15, 'auth', 'user'),
	(16, 'contenttypes', 'contenttype'),
	(17, 'sessions', 'session'),
	(4, 'thread', 'comment'),
	(7, 'thread', 'commentimage'),
	(3, 'thread', 'follow'),
	(2, 'thread', 'like'),
	(8, 'thread', 'likecomment'),
	(10, 'thread', 'notification'),
	(5, 'thread', 'repost'),
	(9, 'thread', 'repostcomment'),
	(1, 'thread', 'thread'),
	(6, 'thread', 'threadimage'),
	(18, 'thumbnail', 'kvstore');

-- Dumping data for table threads_db.django_migrations: ~42 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-03-19 13:37:25.584412'),
	(2, 'auth', '0001_initial', '2025-03-19 13:37:25.888107'),
	(3, 'accounts', '0001_initial', '2025-03-19 13:37:25.932694'),
	(4, 'accounts', '0002_alter_myuser_user', '2025-03-19 13:37:25.939719'),
	(5, 'accounts', '0003_myuser_link_alter_myuser_bio', '2025-03-19 13:37:25.990401'),
	(6, 'accounts', '0004_alter_myuser_profile_picture', '2025-03-19 13:37:25.996334'),
	(7, 'admin', '0001_initial', '2025-03-19 13:37:26.090669'),
	(8, 'admin', '0002_logentry_remove_auto_add', '2025-03-19 13:37:26.097551'),
	(9, 'admin', '0003_logentry_add_action_flag_choices', '2025-03-19 13:37:26.102577'),
	(10, 'contenttypes', '0002_remove_content_type_name', '2025-03-19 13:37:26.166539'),
	(11, 'auth', '0002_alter_permission_name_max_length', '2025-03-19 13:37:26.195884'),
	(12, 'auth', '0003_alter_user_email_max_length', '2025-03-19 13:37:26.211755'),
	(13, 'auth', '0004_alter_user_username_opts', '2025-03-19 13:37:26.216739'),
	(14, 'auth', '0005_alter_user_last_login_null', '2025-03-19 13:37:26.256152'),
	(15, 'auth', '0006_require_contenttypes_0002', '2025-03-19 13:37:26.258424'),
	(16, 'auth', '0007_alter_validators_add_error_messages', '2025-03-19 13:37:26.264572'),
	(17, 'auth', '0008_alter_user_username_max_length', '2025-03-19 13:37:26.303862'),
	(18, 'auth', '0009_alter_user_last_name_max_length', '2025-03-19 13:37:26.342365'),
	(19, 'auth', '0010_alter_group_name_max_length', '2025-03-19 13:37:26.368727'),
	(20, 'auth', '0011_update_proxy_permissions', '2025-03-19 13:37:26.375594'),
	(21, 'auth', '0012_alter_user_first_name_max_length', '2025-03-19 13:37:26.412369'),
	(22, 'sessions', '0001_initial', '2025-03-19 13:37:26.437626'),
	(23, 'thread', '0001_initial', '2025-03-19 13:37:26.846176'),
	(24, 'thread', '0002_delete_imagethread_delete_textthread_and_more', '2025-03-19 13:37:27.056042'),
	(25, 'thread', '0003_remove_thread_image_imagethread', '2025-03-19 13:37:27.128381'),
	(26, 'thread', '0004_alter_imagethread_thread', '2025-03-19 13:37:27.136086'),
	(27, 'thread', '0005_alter_thread_threader', '2025-03-19 13:37:27.145201'),
	(28, 'thread', '0006_alter_comment_user', '2025-03-19 13:37:27.152816'),
	(29, 'thread', '0007_rename_rethread_count_thread_comment_count_and_more', '2025-03-19 13:37:27.358915'),
	(30, 'thread', '0008_rename_rethread_repost_and_more', '2025-03-19 13:37:27.592828'),
	(31, 'thread', '0009_remove_recommentimage_recomment_and_more', '2025-03-19 13:37:27.683994'),
	(32, 'thread', '0010_alter_comment_options_alter_repost_options_and_more', '2025-03-19 13:37:27.746483'),
	(33, 'thread', '0011_rename_threader_thread_user', '2025-03-19 13:37:27.823485'),
	(34, 'thread', '0012_likecomment_likecomment_unique_like_comment', '2025-03-19 13:37:27.906258'),
	(35, 'thread', '0013_alter_like_user', '2025-03-19 13:37:27.914766'),
	(36, 'thread', '0014_alter_likecomment_user', '2025-03-19 13:37:27.922101'),
	(37, 'thread', '0015_comment_liked_users_thread_liked_users_and_more', '2025-03-19 13:37:27.948615'),
	(38, 'thread', '0016_thread_reposted_users', '2025-03-19 13:37:27.957622'),
	(39, 'thread', '0017_remove_thread_repost_count_repostcomment_and_more', '2025-03-19 13:37:28.078731'),
	(40, 'thread', '0018_notification_alter_like_options_and_more', '2025-03-19 13:37:28.205975'),
	(41, 'thread', '0019_alter_commentimage_image_alter_threadimage_image', '2025-03-19 13:37:28.214425'),
	(42, 'thumbnail', '0001_initial', '2025-03-19 13:37:28.224689'),
	(43, 'accounts', '0005_profile', '2025-03-20 12:19:06.067095'),
	(44, 'accounts', '0006_alter_profile_avatar_alter_profile_user', '2025-03-20 12:22:32.182065'),
	(45, 'accounts', '0007_delete_profile', '2025-03-20 12:31:14.267880');

-- Dumping data for table threads_db.django_session: ~5 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('18jmmwhlnlx6mo8um047683eicvm485i', '.eJxVjDsOwjAQBe_iGllrr7MbU9LnDJZ_IQFkS3FSIe5OIqWA9s3Mewvnt3VyW8uLm5O4Cq3E5XcMPj5zOUh6-HKvMtayLnOQhyJP2uRQU37dTvfvYPJt2usOiChBZylkHG1mNjqyHRUB99SlyBqSNYhG75QA1cjQMyKo3noM4vMF08U2bw:1tvTIX:txtRmwR5rLJXJX38EUGcj1yQM7F-An9USKAWwCIm_z4', '2025-04-04 03:43:53.351655'),
	('77psqj6aoeedlaif5yzh38j7f9tcmnf2', '.eJxVjMsOwiAQRf-FtSEwFCwu3fcbmmFmkKqBpI-V8d-1SRe6veec-1IjbmsZt0XmcWJ1UaBOv1tCekjdAd-x3pqmVtd5SnpX9EEXPTSW5_Vw_w4KLuVbGw4-uOgNgQBHhowcz9Y7pJANuD77zrBQiEDWAMZoBZPtJWDuJJF6fwDY3jgr:1tvBJM:--anW-sWNU6uOOxo1p2Ge_Ah9x0Md1IZfJVq3iLPMOM', '2025-04-03 08:31:32.449108'),
	('ms7lwdm9yr3d2ga5v49ndi758jr91fyc', '.eJxVjEEOwiAQRe_C2pDSAtNx6d4zkGGYStVAUtqV8e7apAvd_vfef6lA25rD1mQJc1Jnher0u0Xih5QdpDuVW9Vcy7rMUe-KPmjT15rkeTncv4NMLX9rG3t0BM56B2LRi51MGi33IIQoHZkBRVhG7iIBkB8AvY8mMcBEcVDvD98ROCU:1tvT1G:ovF-eXTGig0M3oIr5bGrReMdomHh-xSGUs8l5EslrKQ', '2025-04-04 03:26:02.900002'),
	('o045u3rqf44o1mthnkqc5z5ruu17hq2c', '.eJxVjMsOwiAQRf-FtSEwFCwu3fcbmmFmkKqBpI-V8d-1SRe6veec-1IjbmsZt0XmcWJ1UaBOv1tCekjdAd-x3pqmVtd5SnpX9EEXPTSW5_Vw_w4KLuVbGw4-uOgNgQBHhowcz9Y7pJANuD77zrBQiEDWAMZoBZPtJWDuJJF6fwDY3jgr:1tvBH0:HTWpT6mh2pR7aBfhDGSI4QNntKH-3xQ91NKc43EBboI', '2025-04-03 08:29:06.742548'),
	('qrunwe120ogbwleb3uke15xr8m4nm8dd', '.eJxVjMEOgjAQRP-lZ9OUdusuHr3zDc22uwpqIKFwMv67kHDQ22Tem3mbxOvSp7XqnAYxFxPM6bfLXJ467kAePN4nW6ZxmYdsd8UetNpuEn1dD_fvoOfab2tHgoShBFKk4ktE8LFpQDwyAUl2W8wqHBsXyJ9bQIwqGaQFx3ozny-_4zdO:1tvBUe:uoTJfVPq_THW-_4xmo0gpRmN40tVeSpPL6yHrNSQCSE', '2025-04-03 08:43:12.710440'),
	('tgklk6waabyol4flbqc3305t3ud5iacx', '.eJxVjMsOwiAQRf-FtSEwFCwu3fcbmmFmkKqBpI-V8d-1SRe6veec-1IjbmsZt0XmcWJ1UaBOv1tCekjdAd-x3pqmVtd5SnpX9EEXPTSW5_Vw_w4KLuVbGw4-uOgNgQBHhowcz9Y7pJANuD77zrBQiEDWAMZoBZPtJWDuJJF6fwDY3jgr:1tvEd6:Ay0WvZSW4yfD2P-K1yHMzTZPGMU2ZMCgsEH53obe3CA', '2025-04-03 12:04:08.269638'),
	('ww0850enoy4eo5n8p9tm4xqc1i2ik6vi', '.eJxVjMsOwiAQRf-FtSEwFCwu3fcbmmFmkKqBpI-V8d-1SRe6veec-1IjbmsZt0XmcWJ1UaBOv1tCekjdAd-x3pqmVtd5SnpX9EEXPTSW5_Vw_w4KLuVbGw4-uOgNgQBHhowcz9Y7pJANuD77zrBQiEDWAMZoBZPtJWDuJJF6fwDY3jgr:1tvCSG:pvicz7GleUJu9kG4rr2cDjWjz6DTdMYLMarC-mtRV5I', '2025-04-03 09:44:48.535307');

-- Dumping data for table threads_db.thread_comment: ~8 rows (approximately)
INSERT INTO `thread_comment` (`id`, `created_at`, `updated_at`, `thread_id`, `user_id`, `comment_count`, `likes_count`, `content`, `parent_comment_id`) VALUES
	(1, '2025-03-19 14:47:52.271185', '2025-03-19 15:11:35.062698', 2, 1, 1, 1, 'Comment bài viết 2', NULL),
	(2, '2025-03-19 14:49:11.718335', '2025-03-19 14:49:11.718335', 2, 1, 0, 0, 'Comment bài viết 2', NULL),
	(5, '2025-03-19 15:11:35.058611', '2025-03-19 15:11:35.058611', 2, 1, 0, 0, 'Nội dung comment rep cmmt 1', 1),
	(6, '2025-03-20 09:18:23.250746', '2025-03-20 09:22:23.894016', 4, 3, 1, 0, 'Đúng vậy!', NULL),
	(7, '2025-03-20 09:19:48.898219', '2025-03-20 09:19:48.898219', 4, 3, 0, 0, 'Mình nói chuẩn vậy ta', NULL),
	(8, '2025-03-20 09:21:15.418578', '2025-03-20 09:21:15.418578', 4, 3, 0, 0, 'Mình nói chuẩn vậy ta', 6),
	(9, '2025-03-20 10:12:50.533100', '2025-03-21 02:38:47.462499', 6, 3, 2, 0, 'Tôi rep user có id 2 để test thông báo', NULL),
	(10, '2025-03-20 10:14:22.913452', '2025-03-20 10:14:22.913452', 6, 3, 0, 0, 'Tôi rep lần 2 cho user có id 2 để test thông báo', NULL),
	(11, '2025-03-20 10:18:46.905446', '2025-03-20 10:18:46.905446', 6, 3, 0, 0, 'Tôi rep lần 3 cho user có id 2 để test thông báo', NULL),
	(12, '2025-03-20 10:25:58.455463', '2025-03-20 10:25:58.455463', 6, 3, 0, 0, 'Tôi rep lần 3 cho user có id 2 để test thông báo', NULL),
	(15, '2025-03-21 02:36:36.723778', '2025-03-21 02:36:36.723778', 6, 3, 0, 0, 'Cài này đâu phải rep, nó là cmt bth thôi', NULL),
	(16, '2025-03-21 02:38:21.779274', '2025-03-21 02:38:21.779274', 6, 3, 0, 0, 'Cài này đâu phải rep, nó là cmt bth thôi', 9),
	(17, '2025-03-21 02:38:47.457992', '2025-03-21 02:38:47.457992', 6, 3, 0, 0, 'Mọa nó, test phát nauwx cho chắc đi', 9),
	(18, '2025-03-21 02:39:59.087085', '2025-03-21 02:39:59.087085', 6, 3, 0, 0, 'Test lại cmt thread', NULL),
	(19, '2025-03-21 03:48:00.510912', '2025-03-21 03:49:35.249438', 9, 21, 1, 0, 'test lại cmt bài 9', NULL),
	(20, '2025-03-21 03:49:35.245438', '2025-03-21 03:49:35.245438', 9, 21, 0, 0, 'test lại rep cmt thread 9', 19),
	(21, '2025-03-21 03:59:21.587547', '2025-03-21 03:59:21.587547', 10, 21, 0, 0, 'test lại respone thread mới', NULL);

-- Dumping data for table threads_db.thread_commentimage: ~0 rows (approximately)

-- Dumping data for table threads_db.thread_follow: ~2 rows (approximately)
INSERT INTO `thread_follow` (`id`, `created_at`, `updated_at`, `followed_id`, `follower_id`) VALUES
	(1, '2025-03-20 09:39:07.762590', '2025-03-20 09:39:07.762590', 2, 3),
	(7, '2025-03-21 04:00:18.530447', '2025-03-21 04:00:18.530447', 2, 21);

-- Dumping data for table threads_db.thread_like: ~3 rows (approximately)
INSERT INTO `thread_like` (`id`, `created_at`, `updated_at`, `thread_id`, `user_id`) VALUES
	(1, '2025-03-19 14:47:20.959359', '2025-03-19 14:47:20.959359', 2, 1),
	(3, '2025-03-20 09:02:37.206911', '2025-03-20 09:02:37.206911', 4, 3),
	(4, '2025-03-20 09:03:02.398763', '2025-03-20 09:03:02.398763', 2, 3),
	(6, '2025-03-21 03:47:38.099152', '2025-03-21 03:47:38.099152', 9, 21);

-- Dumping data for table threads_db.thread_likecomment: ~1 rows (approximately)
INSERT INTO `thread_likecomment` (`id`, `created_at`, `updated_at`, `comment_id`, `user_id`) VALUES
	(1, '2025-03-19 15:05:23.917926', '2025-03-19 15:05:23.917926', 1, 1);

-- Dumping data for table threads_db.thread_notification: ~12 rows (approximately)
INSERT INTO `thread_notification` (`id`, `type`, `content`, `is_read`, `created_at`, `actioner_id`, `user_id`) VALUES
	(1, 'like_thread', 'newuser likes your thread: Bài viết test mới...', 0, '2025-03-20 08:55:21.175144', 3, 1),
	(2, 'repost_thread', 'newuser reposted your thread: Bài viết test mới...', 0, '2025-03-20 08:57:01.662092', 3, 1),
	(3, 'like_thread', 'newuser likes your thread: Bài viết test mới...', 0, '2025-03-20 09:03:02.400449', 3, 1),
	(4, 'follow', 'newuser started following you.', 1, '2025-03-20 09:39:07.765541', 3, 2),
	(5, 'follow', 'newuser started following you.', 0, '2025-03-20 09:40:05.844032', 3, 1),
	(6, 'follow', 'newuser started following you.', 0, '2025-03-20 09:56:23.595308', 3, 1),
	(7, 'follow', 'newuser started following you.', 0, '2025-03-20 09:58:01.102642', 3, 1),
	(8, 'follow', 'newuser started following you.', 0, '2025-03-20 09:59:12.147210', 3, 1),
	(9, 'comment', 'newuser reply to your thread: Test thông báo...', 1, '2025-03-20 10:12:50.537313', 3, 2),
	(10, 'comment', 'newuser reply to your thread: Test thông báo...', 1, '2025-03-20 10:14:22.916959', 3, 2),
	(11, 'comment', 'newuser reply to your thread: Test thông báo...', 1, '2025-03-20 10:18:46.908841', 3, 2),
	(12, 'comment', 'newuser reply to your thread: Test thông báo...', 1, '2025-03-20 10:25:58.458462', 3, 2),
	(13, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:29:50.879718', 3, 2),
	(14, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:30:22.946002', 3, 2),
	(15, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:36:36.727135', 3, 2),
	(16, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:38:21.787517', 3, 2),
	(17, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:38:47.465828', 3, 2),
	(18, 'comment', 'newuser reply to your thread: Test thông báo...', 0, '2025-03-21 02:39:59.090084', 3, 2),
	(19, 'like_thread', 'newuserthanh7 likes your thread: test đăng bài...', 0, '2025-03-21 03:46:15.098991', 21, 2),
	(20, 'like_thread', 'newuserthanh7 likes your thread: test đăng bài...', 0, '2025-03-21 03:47:38.100823', 21, 2),
	(21, 'comment', 'newuserthanh7 reply to your thread: test đăng bài...', 0, '2025-03-21 03:48:00.513488', 21, 2),
	(22, 'comment', 'newuserthanh7 reply to your thread: test đăng bài...', 0, '2025-03-21 03:49:35.251438', 21, 2),
	(23, 'comment', 'newuserthanh7 reply to your thread: test lại đăng post...', 0, '2025-03-21 03:59:21.591904', 21, 3),
	(24, 'follow', 'newuserthanh7 started following you.', 0, '2025-03-21 04:00:18.533471', 21, 2);

-- Dumping data for table threads_db.thread_repost: ~0 rows (approximately)
INSERT INTO `thread_repost` (`id`, `created_at`, `updated_at`, `thread_id`, `user_id`) VALUES
	(1, '2025-03-20 08:57:01.660376', '2025-03-20 08:57:01.660376', 2, 3);

-- Dumping data for table threads_db.thread_repostcomment: ~0 rows (approximately)
INSERT INTO `thread_repostcomment` (`id`, `created_at`, `updated_at`, `comment_id`, `user_id`) VALUES
	(1, '2025-03-20 09:23:04.801919', '2025-03-20 09:23:04.801919', 6, 3);

-- Dumping data for table threads_db.thread_thread: ~9 rows (approximately)
INSERT INTO `thread_thread` (`id`, `likes_count`, `comment_count`, `created_at`, `updated_at`, `user_id`, `content`) VALUES
	(2, 2, 3, '2025-03-19 14:46:48.252325', '2025-03-20 09:03:02.402481', 1, 'Bài viết test mới'),
	(3, 0, 0, '2025-03-20 08:54:31.071790', '2025-03-20 08:54:31.071790', 3, 'Cursor mạnh quá'),
	(4, 1, 2, '2025-03-20 08:57:44.890320', '2025-03-20 09:19:48.909524', 3, 'Cursor mạnh quá'),
	(5, 0, 0, '2025-03-20 08:58:18.352722', '2025-03-20 08:58:18.352722', 3, 'Cursor mạnh quá'),
	(6, 0, 6, '2025-03-20 10:08:41.118493', '2025-03-21 02:39:59.092084', 2, 'Test thông báo'),
	(7, 0, 0, '2025-03-20 10:51:09.827257', '2025-03-20 10:51:09.827257', 3, 'test đăng ảnh'),
	(8, 0, 0, '2025-03-20 12:08:47.714506', '2025-03-20 12:08:47.714506', 3, 'test lại post'),
	(9, 1, 1, '2025-03-20 12:16:02.050454', '2025-03-21 03:48:00.514486', 2, 'test đăng bài'),
	(10, 0, 1, '2025-03-20 13:00:19.295554', '2025-03-21 03:59:21.594947', 3, 'test lại đăng post'),
	(11, 0, 0, '2025-03-21 02:44:51.158468', '2025-03-21 02:44:51.158468', 3, 'Test lưu link ảnh'),
	(12, 0, 0, '2025-03-21 02:51:25.458778', '2025-03-21 02:51:25.458778', 3, 'Test lưu link ảnh 2'),
	(13, 0, 0, '2025-03-21 02:52:55.090665', '2025-03-21 02:52:55.090665', 3, 'Test lưu link ảnh 2'),
	(14, 0, 0, '2025-03-21 03:57:51.301720', '2025-03-21 03:57:51.301720', 21, 'test lại respone thread mới');

-- Dumping data for table threads_db.thread_threadimage: ~0 rows (approximately)
INSERT INTO `thread_threadimage` (`id`, `image`, `thread_id`) VALUES
	(1, 'thread_images/chị_gào_thét_chỉ_con_mèo.webp', 9),
	(2, 'https://example.com/image1.jpg', 11),
	(3, 'https://example.com/image2.jpg', 11),
	(4, 'https://example.com/image1.jpg', 12),
	(5, 'https://example.com/image2.jpg', 12),
	(6, 'https://example.com/image1.jpg', 13),
	(7, 'https://example.com/image2.jpg', 13),
	(8, 'https://example.com/image1.jpg', 14);

-- Dumping data for table threads_db.thumbnail_kvstore: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
