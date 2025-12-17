
-- ============================================
-- HEMNET DATABASE SEED DATA
-- ============================================

-- 1. USERS
INSERT INTO users (email, password_hash, first_name, last_name, phone, user_type, role) VALUES
('erik.andersson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Erik', 'Andersson', '0701234567', 'private', 'buyer'),
('anna.bergstrom@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Anna', 'Bergström', '0701234568', 'private', 'seller'),
('lars.nilsson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Lars', 'Nilsson', '0701234569', 'private', 'buyer'),
('maria.johansson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Maria', 'Johansson', '0701234570', 'private', 'seller'),
('peter.svensson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Peter', 'Svensson', '0701234571', 'private', 'buyer'),
('karin.lundgren@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Karin', 'Lundgren', '0701234572', 'private', 'buyer'),
('johan.karlsson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Johan', 'Karlsson', '0701234573', 'business', 'agent'),
('sara.persson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Sara', 'Persson', '0701234574', 'business', 'agent'),
('mikael.gustafsson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Mikael', 'Gustafsson', '0701234575', 'business', 'agent'),
('linda.olsson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Linda', 'Olsson', '0701234576', 'business', 'agent'),
('admin@hemnet.se', '$2b$10$abcdefghijklmnopqrstuv', 'Admin', 'User', '0701234577', 'internal', 'admin'),
('emma.hansen@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Emma', 'Hansen', '0701234578', 'private', 'buyer'),
('oscar.lindberg@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Oscar', 'Lindberg', '0701234579', 'private', 'seller'),
('sofia.eriksson@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Sofia', 'Eriksson', '0701234580', 'private', 'buyer'),
('anders.berg@email.se', '$2b$10$abcdefghijklmnopqrstuv', 'Anders', 'Berg', '0701234581', 'business', 'agent');

-- 2. REALTOR AGENCIES
INSERT INTO realtor_agencies (name, license_number, description, phone, email, address, city, postal_code, website) VALUES
('Svensk Fastighetsförmedling Stockholm', 'SFF-STH-001', 'Ledande fastighetsmäklare i Stockholm med över 30 års erfarenhet', '08-1234567', 'info@svenskfast-sthlm.se', 'Strandvägen 12', 'Stockholm', '114 56', 'www.svenskfast-sthlm.se'),
('Mäklarhuset Göteborg', 'MH-GBG-002', 'Din pålitliga partner för fastighetsaffärer i Göteborg', '031-7654321', 'kontakt@maklarhuset-gbg.se', 'Avenyn 45', 'Göteborg', '411 36', 'www.maklarhuset-gbg.se'),
('Erik Olsson Fastighetsförmedling', 'EOF-003', 'Personlig service och bred marknadskännedom', '08-9876543', 'info@erikolsson.se', 'Karlavägen 60', 'Stockholm', '114 49', 'www.erikolsson.se'),
('Länsförsäkringar Fastighetsförmedling', 'LFF-004', 'Trygg fastighetsförmedling med lokala mäklare', '08-5555555', 'fastighet@lansforsakringar.se', 'Tegeluddsvägen 11-13', 'Stockholm', '115 82', 'www.lansforsakringar.se'),
('Fastighetsbyrån Malmö', 'FB-MMO-005', 'Skånes största fastighetsmäklare', '040-123456', 'malmo@fastighetsbyran.se', 'Södergatan 24', 'Malmö', '211 34', 'www.fastighetsbyran.se');

-- 3. REALTOR AGENTS
INSERT INTO realtor_agent (agency_id, user_id, bio, profile_image_url, years_experience) VALUES
(1, 7, 'Erfaren mäklare specialiserad på lyxlägenheter i Stockholm', 'https://example.com/agents/johan.jpg', 12),
(1, 8, 'Expertis inom villor och radhus i Stockholms förorter', 'https://example.com/agents/sara.jpg', 8),
(2, 9, 'Specialist på bostadsrätter i centrala Göteborg', 'https://example.com/agents/mikael.jpg', 15),
(3, 10, 'Fokuserar på förstagångsköpare och yngre familjer', 'https://example.com/agents/linda.jpg', 5),
(4, 15, 'Bred erfarenhet av alla typer av bostäder', 'https://example.com/agents/anders.jpg', 20);

-- 4. LISTING CATEGORIES
INSERT INTO listing_categories (name, description) VALUES
('Lägenhet', 'Bostadsrätter och hyresrätter'),
('Villa', 'Fristående villor'),
('Radhus', 'Radhus och kedjehus'),
('Fritidshus', 'Sommarstugor och fritidsbostäder'),
('Tomt', 'Tomter för nybyggnation'),
('Gård', 'Lantbruk och gårdar'),
('Parhus', 'Parhus och tvåfamiljshus');

-- 5. HOUSE LISTINGS
INSERT INTO house_listing (agent_id, category_id, user_id, title, description, price, address, city, postal_code, rooms, size_sqm, plot_size_sqm, year_built, floor, balcony, monthly_fee, operating_cost, latitude, longitude, status, published_at) VALUES
-- Stockholm Listings
(1, 1, 2, 'Lyxig takvåning med utsikt över Djurgården', 'Exklusiv takvåning i toppskick med fantastisk utsikt över Djurgården och vattnet. Ljusa och luftiga rum med öppen planlösning mellan kök och vardagsrum. Två stora balkonger på totalt 40 kvm. Walking distance till Stureplan och Östermalms torg.', 15900000, 'Strandvägen 45', 'Stockholm', '114 56', 4.5, 145, NULL, 1912, 6, true, 6500, 0, 59.3334, 18.0845, 'active', '2024-12-01 10:00:00'),

(1, 1, 4, 'Charmig 2a vid Mariatorget', 'Ljus och välplanerad tvåa i klassiskt sekelskifteshus. Högt i tak, vackra originaldetaljer och modernt kök. Lugnt läge på innergård med utsikt mot grönskande trädgårdar. Perfekt för singel eller par.', 4750000, 'Hornsgatan 78', 'Stockholm', '118 21', 2, 58, NULL, 1898, 3, false, 3200, 0, 59.3165, 18.0621, 'active', '2024-12-05 14:30:00'),

(2, 2, 4, 'Familjevilla med pool i Danderyd', 'Vacker villa i naturskönt läge med egen pool och stor tomt. Genomgående renoverad 2020. Öppet kök mot vardagsrum med utgång till altan. 5 sovrum varav 2 på nedre plan. Dubbelgarage och laddbox för elbil.', 18500000, 'Enebyvägen 23', 'Danderyd', '182 32', 7, 240, 1200, 1985, NULL, false, 0, 45000, 59.3981, 18.0344, 'active', '2024-11-28 09:00:00'),

(2, 3, 2, 'Modernt radhus i Bromma', 'Nybyggt radhus i två plan med smart planlösning. Stora fönsterpartier som släpper in mycket ljus. Egen uteplats och förråd. Nära till Brommaplan och goda kommunikationer.', 7900000, 'Ulvsundavägen 156', 'Bromma', '168 67', 5, 130, 85, 2022, NULL, true, 4100, 0, 59.3378, 17.9401, 'active', '2024-12-10 11:00:00'),

(1, 1, 13, 'Stilren etta på Kungsholmen', 'Totalrenoverad ettan i modernt utförande. Öppet kök med köksö, helkaklat badrum med tvättmaskin. Fantastiskt läge nära Rådhuset och Norr Mälarstrand.', 3250000, 'Hantverkargatan 34', 'Stockholm', '112 21', 1, 38, NULL, 1935, 4, true, 2800, 0, 59.3301, 18.0298, 'active', '2024-12-08 13:00:00'),

-- Göteborg Listings
(3, 1, 4, 'Vindsvåning i Haga', 'Unik vindsvåning med synliga takbjälkar och industriell känsla. Totalrenoverad med bibehållna charm. Två sovrum och stort vardagsrum. Egen takterrass med vacker utsikt över Haga.', 6200000, 'Haga Nygata 15', 'Göteborg', '413 01', 3, 95, NULL, 1890, 5, true, 3900, 0, 57.6989, 11.9539, 'active', '2024-12-03 10:30:00'),

(3, 1, 2, 'Trea med havsutsikt i Saltholmen', 'Ljus och fräsch lägenhet med fantastisk havsutsikt från balkong och vardagsrum. Nyrenoverat kök och badrum. Garage i källaren ingår. Perfekt för dig som älskar havet och vill bo nära skärgården.', 5100000, 'Saltholmsvägen 89', 'Göteborg', '426 76', 3, 82, NULL, 1976, 4, true, 4200, 0, 57.6465, 11.8347, 'active', '2024-11-30 15:00:00'),

(3, 2, 4, 'Klassisk Göteborgsvillan i Örgryte', 'Charmig sekelskiftesvillan med många originaldetaljer bevarade. Kakelugnar, stuckaturer och vackra parkettgolv. Stor trädgård med äppelträd och stenlagd uteplats. Central men ändå lugnt läge.', 12800000, 'Societetsgatan 22', 'Göteborg', '413 27', 6, 180, 650, 1908, NULL, false, 0, 38000, 57.6957, 12.0067, 'active', '2024-12-07 09:30:00'),

-- Malmö Listings
(4, 1, 2, 'Modern lägenhet vid Västra Hamnen', 'Ljus och rymlig nybyggnation med öppen planlösning. Panoramafönster med havsutsikt. Balkong i söderläge. Hög standard med golvvärme och smarta lösningar. Nära till Turning Torso och stranden.', 4850000, 'Stapelbäddsgatan 5', 'Malmö', '211 19', 3, 88, NULL, 2018, 7, true, 4600, 0, 55.6134, 12.9843, 'active', '2024-12-06 12:00:00'),

(4, 3, 4, 'Fint radhus i Limhamn', 'Välskött radhus i barnvänligt område. Tre sovrum på övervåning. Stort kök med plats för matbord. Egen trädgård och uteplats i söderläge. Garage och förråd. Nära till strand och bra förskolor.', 5600000, 'Kalkbrottsgatan 12', 'Malmö', '216 16', 5, 118, 120, 1994, NULL, false, 3100, 0, 55.5678, 12.9234, 'active', '2024-12-02 14:00:00'),

-- More varied listings
(2, 4, 13, 'Mysig sommarstuga vid Mälaren', 'Charmig röd sommarstuga i lugnt läge vid vattnet. Egen brygga och stor tomt. Vedeldad bastu. Perfekt som fritidsbostad för familjen. Renoverad 2019 med bibehållen charm.', 2850000, 'Strandvägen 42', 'Ekerö', '178 93', 3, 65, 800, 1952, NULL, false, 0, 8000, 59.2789, 17.8012, 'active', '2024-11-25 10:00:00'),

(5, 2, 4, 'Arkitektritad villa i Bjärred', 'Exklusiv designvilla ritad av känt arkitektkontor. Stora glaspartier, öppen planlösning och genomtänkt funktionalitet. Pool, poolhus och välsködd trädgård. Havsutsikt från flera rum.', 16900000, 'Strandvägen 88', 'Bjärred', '237 35', 6, 280, 1500, 2015, NULL, false, 0, 55000, 55.7534, 13.0456, 'active', '2024-12-04 11:30:00'),

(1, 1, 2, 'Studentvänlig etta i Vasastan', 'Praktisk och fräsch etta perfekt för student eller yngre person. Nära till universitet och goda kommunikationer. Tvättstuga i källaren. Låg avgift.', 2450000, 'Odengatan 94', 'Stockholm', '113 22', 1, 32, NULL, 1948, 2, false, 2100, 0, 59.3456, 18.0543, 'active', '2024-12-09 16:00:00'),

(3, 1, 4, 'Påkostad 4a i Linnéstaden', 'Fantastisk lägenhet i absolut toppskick. Totalrenoverad med kvalitetsmaterial. Öppet modernt kök, marmorbadrum, ekparkett och smart belysning. Balkong mot lugn innergård.', 7400000, 'Linnégatan 36', 'Göteborg', '413 04', 4, 110, NULL, 1903, 3, true, 4800, 0, 57.6978, 11.9534, 'active', '2024-12-01 13:30:00'),

(2, 3, 2, 'Rymligt parhus i Täby', 'Välplanerat parhus i två plan. Ljust och fräscht med renoverat kök 2021. Fyra sovrum och två badrum. Stor altan och trädgård. Barnvänligt område med nära till skolor och natur.', 8900000, 'Enhagsvägen 15', 'Täby', '183 52', 6, 155, 250, 1988, NULL, false, 3600, 0, 59.4389, 18.0712, 'active', '2024-11-29 10:30:00');

-- 6. LISTING IMAGES
INSERT INTO listing_images (listing_id, image_url, display_order, is_primary, caption) VALUES
-- Images for Listing 1 (Lyxig takvåning)
(1, 'https://example.com/listings/1/image1.jpg', 1, true, 'Vardagsrum med utsikt över Djurgården'),
(1, 'https://example.com/listings/1/image2.jpg', 2, false, 'Modernt kök med öppen planlösning'),
(1, 'https://example.com/listings/1/image3.jpg', 3, false, 'Sovrum med inbyggda garderober'),
(1, 'https://example.com/listings/1/image4.jpg', 4, false, 'Takterrass med kvällssol'),
(1, 'https://example.com/listings/1/image5.jpg', 5, false, 'Lyxigt badrum med tvättmaskin'),

-- Images for Listing 2 (Charmig 2a)
(2, 'https://example.com/listings/2/image1.jpg', 1, true, 'Ljust vardagsrum med högt i tak'),
(2, 'https://example.com/listings/2/image2.jpg', 2, false, 'Modernt kök'),
(2, 'https://example.com/listings/2/image3.jpg', 3, false, 'Sovrum med utsikt mot innergård'),

-- Images for Listing 3 (Familjevilla)
(3, 'https://example.com/listings/3/image1.jpg', 1, true, 'Fasad med pool'),
(3, 'https://example.com/listings/3/image2.jpg', 2, false, 'Öppet kök och vardagsrum'),
(3, 'https://example.com/listings/3/image3.jpg', 3, false, 'Master bedroom'),
(3, 'https://example.com/listings/3/image4.jpg', 4, false, 'Pool och poolhus'),

-- Images for Listing 4 (Modernt radhus)
(4, 'https://example.com/listings/4/image1.jpg', 1, true, 'Modern fasad'),
(4, 'https://example.com/listings/4/image2.jpg', 2, false, 'Vardagsrum med stora fönster'),
(4, 'https://example.com/listings/4/image3.jpg', 3, false, 'Kök med köksö'),

-- Images for remaining listings (2-3 images each)
(5, 'https://example.com/listings/5/image1.jpg', 1, true, 'Öppet kök med köksö'),
(5, 'https://example.com/listings/5/image2.jpg', 2, false, 'Vardagsrum'),

(6, 'https://example.com/listings/6/image1.jpg', 1, true, 'Vardagsrum med takbjälkar'),
(6, 'https://example.com/listings/6/image2.jpg', 2, false, 'Takterrass'),
(6, 'https://example.com/listings/6/image3.jpg', 3, false, 'Sovrum'),

(7, 'https://example.com/listings/7/image1.jpg', 1, true, 'Havsutsikt från balkongen'),
(7, 'https://example.com/listings/7/image2.jpg', 2, false, 'Vardagsrum'),

(8, 'https://example.com/listings/8/image1.jpg', 1, true, 'Klassisk fasad'),
(8, 'https://example.com/listings/8/image2.jpg', 2, false, 'Kakelugn i vardagsrummet'),
(8, 'https://example.com/listings/8/image3.jpg', 3, false, 'Trädgård'),

(9, 'https://example.com/listings/9/image1.jpg', 1, true, 'Panoramautsikt'),
(9, 'https://example.com/listings/9/image2.jpg', 2, false, 'Öppet kök'),

(10, 'https://example.com/listings/10/image1.jpg', 1, true, 'Fasad'),
(10, 'https://example.com/listings/10/image2.jpg', 2, false, 'Trädgård och uteplats');

-- 7. BIDS
INSERT INTO bids (listing_id, user_id, amount, bid_date, status, comment) VALUES
(1, 1, 15500000, '2024-12-11 14:30:00', 'pending', 'Vill gärna få en visning innan jag höjer mitt bud'),
(1, 3, 15900000, '2024-12-12 09:15:00', 'pending', 'Intresserad av ett snabbt köp'),
(2, 5, 4650000, '2024-12-10 16:20:00', 'rejected', 'För lågt enligt säljare'),
(2, 6, 4750000, '2024-12-11 11:00:00', 'accepted', 'Accepterat bud'),
(3, 1, 18200000, '2024-12-08 10:30:00', 'pending', 'Kontantköp möjligt'),
(4, 5, 7800000, '2024-12-13 13:45:00', 'pending', NULL),
(5, 12, 3200000, '2024-12-12 15:00:00', 'pending', 'Förstagångsköpare'),
(6, 3, 6100000, '2024-12-09 12:20:00', 'pending', NULL),
(7, 6, 5050000, '2024-12-10 14:00:00', 'pending', 'Kan flytta in direkt'),
(9, 14, 4800000, '2024-12-11 10:30:00', 'pending', NULL);

-- 8. FAVORITES
INSERT INTO favorites (listing_id, user_id) VALUES
(1, 1),
(1, 5),
(2, 1),
(3, 1),
(3, 3),
(4, 5),
(5, 6),
(5, 12),
(6, 3),
(6, 14),
(7, 6),
(8, 1),
(8, 3),
(9, 14),
(10, 5),
(11, 1),
(12, 3),
(13, 14),
(14, 6),
(15, 1);

-- 9. AGENT REVIEWS
INSERT INTO agent_reviews (agent_id, user_id, rating, comment, transaction) VALUES
(1, 1, 5, 'Johan var extremt professionell och hjälpte oss hitta vår drömlägenhet. Rekommenderas varmt!', 'purchase'),
(1, 3, 5, 'Utmärkt service från början till slut. Kunnig och snabb i sin kommunikation.', 'purchase'),
(2, 5, 4, 'Bra mäklare som lyssnade på våra behov. Lite långsam respons ibland.', 'purchase'),
(2, 2, 5, 'Sara sålde vår villa snabbt och till bra pris. Mycket nöjd!', 'sale'),
(3, 6, 5, 'Mikael känner Göteborg som sin egen ficka. Hittade perfekt lägenhet åt oss!', 'purchase'),
(3, 4, 4, 'Professionell och trevlig. Sålde vår lägenhet över utgångspris.', 'sale'),
(4, 12, 5, 'Linda var fantastisk att arbeta med som förstagångsköpare. Förklarade allt noggrant.', 'purchase'),
(4, 14, 4, 'Bra bemötande och god marknadskännedom.', 'purchase'),
(5, 1, 3, 'Okej mäklare men kunde varit mer engagerad i processen.', 'sale');

-- 10. VIEWING BOOKINGS
INSERT INTO viewing_booking (listing_id, user_id, viewing_date, viewing_time, status, notes) VALUES
(1, 1, '2024-12-18', '2024-12-18 17:00:00', 'confirmed', 'Vill se lägenhet i kvällsljus'),
(1, 5, '2024-12-18', '2024-12-18 17:30:00', 'confirmed', NULL),
(2, 6, '2024-12-17', '2024-12-17 16:00:00', 'completed', 'Intresserad av att lägga bud'),
(3, 1, '2024-12-19', '2024-12-19 14:00:00', 'confirmed', 'Kommer med familjen'),
(3, 3, '2024-12-19', '2024-12-19 15:00:00', 'confirmed', NULL),
(4, 5, '2024-12-20', '2024-12-20 18:00:00', 'pending', 'Önskar längre visningstid'),
(5, 12, '2024-12-16', '2024-12-16 17:00:00', 'completed', NULL),
(6, 3, '2024-12-21', '2024-12-21 13:00:00', 'confirmed', NULL),
(6, 14, '2024-12-21', '2024-12-21 14:00:00', 'confirmed', 'Intresserad av teknisk status'),
(7, 6, '2024-12-17', '2024-12-17 15:00:00', 'completed', NULL),
(8, 1, '2024-12-22', '2024-12-22 11:00:00', 'confirmed', 'Vill se trädgården'),
(9, 14, '2024-12-19', '2024-12-19 16:00:00', 'confirmed', NULL),
(10, 5, '2024-12-20', '2024-12-20 17:00:00', 'confirmed', 'Intresserad av närområdet'),
(11, 1, '2024-12-23', '2024-12-23 10:00:00', 'pending', NULL),
(12, 3, '2024-12-28', '2024-12-28 14:00:00', 'pending', 'Efter jul'),
(1, 12, '2024-12-15', '2024-12-15 16:00:00', 'cancelled', 'Kunde inte komma');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check record counts
- SELECT 'users' as table_name, COUNT(*) as count FROM users
-- UNION ALL
-- SELECT 'realtor_agencies', COUNT(*) FROM realtor_agencies
-- UNION ALL
-- SELECT 'realtor_agent', COUNT(*) FROM realtor_agent
-- UNION ALL
-- SELECT 'listing_categories', COUNT(*) FROM listing_categories
-- UNION ALL
-- SELECT 'house_listing', COUNT(*) FROM house_listing
-- UNION ALL
-- SELECT 'listing_images', COUNT(*) FROM listing_images
-- UNION ALL
-- SELECT 'bids', COUNT(*) FROM bids
-- UNION ALL
-- SELECT 'favorites', COUNT(*) FROM favorites
-- UNION ALL
-- SELECT 'agent_reviews', COUNT(*) FROM agent_reviews
-- UNION ALL
-- SELECT 'viewing_booking', COUNT(*) FROM viewing_booking;