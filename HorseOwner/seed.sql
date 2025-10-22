INSERT INTO horses (name, breed, sex, birth_date, color, origin, notes) VALUES
('Namira', 'QH', 'mare', '2016-04-25', 'smoky cream', 'PL', 'Spokojna, western'),
('Wiosenka', 'Kuc Walijski', 'mare', '2017-06-12', 'myszata', 'PL', 'Energiczna, teren'),
('Moro', 'SP', 'gelding','2009-05-05','black', 'PL', 'Spokojny, ujeżdżenie');

-- Mapowanie nazw -> ID (SQLite: prosto wybierzemy ID przez subquery w INSERTach)
-- Zakładamy, że w bazie po seedzie koni: Namira ma id=1, Wiosenka id=2.
-- Jeśli nie masz gwarancji ID, używamy subselectów po name.

INSERT INTO trainings (horse_id, date, time, duration_min, type, score, satisfied, notes)
VALUES
  -- 2025-10-20
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-20', '09:30', 45, 'dressage',   7, 1, 'Przejścia stęp-kłus, dobra reakcja na łydkę'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-20', '11:30', 50, 'dressage',   6, 1, 'Praca nad ustawieniem szyi, półparady'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-20', '17:15', 60, 'trail',      6, 1, 'Spokojny teren, praca nad rytmem'),

  -- 2025-10-19
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-19', '10:05', 50, 'groundwork', 8, 1, 'Lonża, ustępowania, elastyczność szyi'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-19', '12:15', 40, 'groundwork', 7, 1, 'Lonża, ustępowania na kole'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-19', '16:40', 40, 'dressage',   5, 0, 'Parę spięć, trudność z kontaktem'),

  -- 2025-10-18
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-18', '08:50', 55, 'dressage',   6, 1, 'Ustabilizowany takt w kłusie'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-18', '09:40', 55, 'trail',      6, 1, 'Teren spokojny, kontrola tempa'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-18', '18:10', 70, 'trail',      7, 1, 'Dłuższy galop, dobra kondycja'),

  -- 2025-10-17
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-17', '09:10', 40, 'jumping',    6, 1, 'Małe krzyżyki, rytm nierówny na początku'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-17', '10:20', 35, 'other',      5, 0, 'Spacer w ręku + stretching'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-17', '15:20', 35, 'groundwork', 5, 0, 'Rozproszenia, praca nad skupieniem'),

  -- 2025-10-16
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-16', '10:20', 30, 'other',      6, 1, 'Spacer w ręku + stretching'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-16', '11:10', 45, 'dressage',   7, 1, 'Przejścia kłus–stęp, stabilny kontakt'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-16', '17:00', 50, 'dressage',   7, 1, 'Łuki, koła 15 m, stabilny kontakt'),

  -- 2025-10-15
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-15', '08:55', 40, 'jumping',    5, 0, 'Małe drążki, delikatnie spięty'),
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-15', '09:00', 45, 'dressage',   8, 1, 'Lepsze przejścia kłus-galop'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-15', '18:20', 55, 'trail',      6, 1, 'Podjazdy, zjazdy, kontrola tempa'),

  -- 2025-10-14
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-14', '10:45', 60, 'jumping',    7, 1, 'Seria cavaletti, poprawa koordynacji'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-14', '12:30', 30, 'other',      6, 1, 'Rozprężenie, praca nad rozluźnieniem'),
  ((SELECT id FROM horses WHERE name='Wiosenka'), '2025-10-14', '16:30', 30, 'other',      4, 0, 'Krótki spacer, niska motywacja'),

  -- 2025-10-13
  ((SELECT id FROM horses WHERE name='Namira'),   '2025-10-13', '09:35', 50, 'dressage',   7, 1, 'Ustępowania od łydki, ładne półparady'),
  ((SELECT id FROM horses WHERE name='Moro'),     '2025-10-13', '10:25', 50, 'dressage',   7, 1, 'Ustępowania od łydki, równy takt');

-- =========================================
-- TREATMENTS SEED (Namira, Wiosenka)
-- 5 DONE (status=1) + 3 PLANNED (status=0) per horse
-- =========================================

-- Namira – done
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Namira'),'Werkowanie','2025-09-10',0,'Kowal Nowak'),
((SELECT id FROM horses WHERE name='Namira'),'Szczepienie','2025-03-15',1,'Flu/Tetanus'),
((SELECT id FROM horses WHERE name='Namira'),'Odrobaczenie','2025-07-01',1,'Ivermectin'),
((SELECT id FROM horses WHERE name='Namira'),'Kontrola zębów','2025-06-05',1,'Równanie kłów'),
((SELECT id FROM horses WHERE name='Namira'),'Fizjoterapia','2025-08-20',1,'Rozluźnienie grzbietu');

-- Namira – planned
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Namira'),'Werkowanie','2025-10-25',0,'Co ~6 tyg.'),
((SELECT id FROM horses WHERE name='Namira'),'Szczepienie','2025-11-05',0,'Booster'),
((SELECT id FROM horses WHERE name='Namira'),'Odrobaczenie','2025-12-15',0,'Zgodnie z grafikiem');

-- Wiosenka – done
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Wiosenka'),'Werkowanie','2025-09-12',0,'Kowal Nowak'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Szczepienie','2025-03-18',1,'Flu/Tetanus'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Odrobaczenie','2025-07-03',1,'Ivermectin'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Kontrola zębów','2025-06-10',1,'Delikatne korekty'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Fizjoterapia','2025-08-22',1,'Taping ogonowo-krzyżowy');

-- Wiosenka – planned
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Wiosenka'),'Werkowanie','2025-10-26',0,'Co ~6 tyg.'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Szczepienie','2025-11-08',0,'Booster'),
((SELECT id FROM horses WHERE name='Wiosenka'),'Odrobaczenie','2025-12-17',0,'Zgodnie z grafikiem');

-- MORO – done
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Moro'),'Werkowanie','2025-09-08',0,'Kowal Nowak'),
((SELECT id FROM horses WHERE name='Moro'),'Szczepienie','2025-03-20',1,'Flu/Tetanus'),
((SELECT id FROM horses WHERE name='Moro'),'Odrobaczenie','2025-07-05',1,'Ivermectin'),
((SELECT id FROM horses WHERE name='Moro'),'Kontrola zębów','2025-06-12',1,'Równanie kłów'),
((SELECT id FROM horses WHERE name='Moro'),'Fizjoterapia','2025-08-25',1,'Rozluźnienie grzbietu');

-- MORO – planned
INSERT INTO treatments (horse_id, name, date, status, notes) VALUES
((SELECT id FROM horses WHERE name='Moro'),'Werkowanie','2025-10-27',0,'Co ~6 tyg.'),
((SELECT id FROM horses WHERE name='Moro'),'Szczepienie','2025-11-10',0,'Booster'),
((SELECT id FROM horses WHERE name='Moro'),'Odrobaczenie','2025-12-18',0,'Zgodnie z grafikiem');
