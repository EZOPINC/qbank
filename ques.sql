-- Question Bank import: 43 questions (30 with answers from the printed answer sheets)
-- Source: DocScanner_27_Oct_2026_12-08_pm.pdf (Ch12 Q9-22, Ch13 Q1-8)
--         DocScanner_27_Oct_2026_12-10_pm.pdf (Ch16 Q9-11, Ch17 Q1-13, Ch18 Q1-5)
-- Run AFTER `python manage.py migrate`.   psql -U qbank -d qbank -f question_bank_import.sql
-- Safe to re-run: content_hash is unique, duplicates are skipped.
-- correct_answer is NULL where the page showed no answer sheet (Ch13, Ch18). All rows are 'needs_review'.
BEGIN;
INSERT INTO bank_question (
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_answer,
        explanation,
        difficulty_level,
        language,
        source_question_number,
        content_hash,
        review_status,
        created_at,
        updated_at
    )
VALUES -- Ch12 Q9 (12-08_pm.pdf)
    (
        'The first leader to use the word ''Swaraj'' was',
        'Bal Gangadhar Tilak',
        'Lala Lajpat Rai',
        'Dayanand Saraswati',
        'Mahatma Gandhi',
        'C',
        '',
        '',
        'en',
        9,
        '8afdac07869e35040eef835634d3a1c3ce913bdb059a6929325d08eac6162495',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q10 (12-08_pm.pdf)
    (
        'First Indian elected to the British House of Commons was Dadabhai Naoroji who contested on the ticket of',
        'Liberal Party',
        'Labour Party',
        'Conservative Party',
        'Communist Party',
        'A',
        '',
        '',
        'en',
        10,
        '87adb0daddc9388a20d0a026c2aee807656288e842103aa726b5dbeeef4f74f6',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q11 (12-08_pm.pdf)
    (
        'Who was called the ''Grand Old Man of India''?',
        'Dadabhai Naoroji',
        'Gopal Krishna Gokhale',
        'Ramesh Chandra Banerjee',
        'Sir Syed Ahmad Khan',
        'A',
        '',
        '',
        'en',
        11,
        'd3ff8904048147a9d60460ac5de7fd977869fd35cf8deed2a485ea2a4cf20b21',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q12 (12-08_pm.pdf)
    (
        'Who among the following is known by the title of ''The Grand Old Man''?',
        'Khan Abdul Ghaffar Khan',
        'W.C. Banerjee',
        'Dadabhai Naoroji',
        'Motilal Nehru',
        'C',
        '',
        '',
        'en',
        12,
        'aacffd649ed8904481403041dc32b9b3e21dde1f3f562c7e378a9d4b2fae3d1b',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q13 (12-08_pm.pdf)
    (
        'Which one of the following statements is not correct about Dadabhai Naoroji?',
        'He wrote a book ''Poverty and Un-British Rule in India''',
        'He worked as a Professor of Gujarati in the University College, London',
        'He laid the foundation of woman''s education in Bombay',
        'He was elected as a member of British Parliament on the ticket of the Conservative Party',
        'D',
        '',
        '',
        'en',
        13,
        '20952cc910ebca85c7c0019d728a2b3fdae0001c3bc19535cc137bfbedc7f40c',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q14 (12-08_pm.pdf)
    (
        'Which one of the following statements is not correct about Dadabhai Naoroji?',
        'He was the first Indian to be appointed as Professor of Mathematics and Physics at Elphinstone College, Bombay',
        'He was elected as the member of British Parliament in 1892',
        'He started a Gujarati Journal, ''Rast Goftar''',
        'For four times he had presided over the Indian National Congress',
        'D',
        '',
        '',
        'en',
        14,
        '7c9647ed4b11f88974216717b88230d96727d2335cbecc53b61fb016e692f797',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q15 (12-08_pm.pdf)
    (
        'At which session was the Indian National Congress (INC) divided into two groups - ''Naram Dal'' and ''Garam Dal''?',
        'Bombay',
        'Surat',
        'Allahabad',
        'Lahore',
        'B',
        '',
        '',
        'en',
        15,
        '346fc77deaed8be6c96aabe9b8685c036759054686b2bff38fe0269b94f9730d',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q16 (12-08_pm.pdf)
    (
        'Where did the Indian Congress got divided into two wings moderates and extremists?',
        'Surat Session, 1907',
        'Lahore Session, 1909',
        'Calcutta Session, 1911',
        'Karachi Session, 1913',
        'A',
        '',
        '',
        'en',
        16,
        'c9d895ac85f356dd2d21b492aaa7923021d66a01f19bbe75a2b5cb2a6b66811e',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q17 (12-08_pm.pdf)
    (
        'The President of the Surat Session of Indian National Congress (1907) was',
        'Dadabhai Naoroji',
        'Bal Gangadhar Tilak',
        'Gopal Krishna Gokhale',
        'R.B. Ghosh',
        'D',
        '',
        '',
        'en',
        17,
        'f0edb79d71bf28a187b57758e76726e036001724e73640be3c9d81ebd42b268c',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q18 (12-08_pm.pdf)
    (
        'Four resolutions were passed at the famous Calcutta Session of Indian National Congress in 1906. The question of either retention or rejection of these four resolutions became the cause of a split in Congress at the next Congress Session held in Surat in 1907.
Which one of the following was not one of those resolutions?',
        'Annulment of partition of Bengal',
        'Boycott',
        'National education',
        'Swadeshi',
        'A',
        '',
        '',
        'en',
        18,
        '7366e72b3e109080c21309155fdfbec4bf409a9ad805ddc29cdfb5f84ff5ce65',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q19 (12-08_pm.pdf)
    (
        'The process of split in the Congress in the early years of the twentieth century began over',
        'Strategies of the Congress Movement',
        'Objectives of the Congress',
        'Participation of the people in the Congress Movement',
        'All of the above',
        'D',
        '',
        '',
        'en',
        19,
        'f01c9ee746ee6a4d7f39fb761bd370e57af9292db804a5b258b221250d78fce0',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q20 (12-08_pm.pdf)
    (
        '''Split of Surat'' in Indian National Congress was held in',
        '1905',
        '1906',
        '1907',
        '1908',
        'C',
        '',
        '',
        'en',
        20,
        'e806cadde0750a616afdd840efaaa76edbd90d754ac3437066b860cb6ff468b1',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q21 (12-08_pm.pdf)
    (
        'Surat split was led by',
        'Hume',
        'Dufferin',
        'Tilak',
        'Gandhiji',
        'C',
        '',
        '',
        'en',
        21,
        'c775e4cfdd234e768a38c535b65a082d260ac49f73e6be9c9263156d035fe8fb',
        'needs_review',
        now(),
        now()
    ),
    -- Ch12 Q22 (12-08_pm.pdf)
    (
        'What was the main reason for the split in the Indian National Congress at Surat in 1907?',
        'Introduction of communalism into Indian politics by Lord Minto',
        'Extremists'' lack of faith in the capacity of the moderates to negotiate with the British Government',
        'Foundation of Muslim League',
        'Aurobindo Ghosh''s inability to be elected as the President of the Indian National Congress',
        'B',
        '',
        '',
        'en',
        22,
        'af32882ec3f54122db6f3b63b0af332be2b8c9685341b408da0c3543e6d39055',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q1 (12-08_pm.pdf)
    (
        'In 1906 Muslim League was founded at',
        'Lahore',
        'Delhi',
        'Calcutta',
        'Dhaka',
        NULL,
        '',
        '',
        'en',
        1,
        '2dae38d8ff176124eba24197ccf0bed0394db70c0a2ff24d84fef723f3e12599',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q2 (12-08_pm.pdf)
    (
        'All India Muslim League was founded in the year',
        '1905',
        '1904',
        '1907',
        '1906',
        NULL,
        '',
        '',
        'en',
        2,
        'c9f86fd050a3ed2b0a2c58878a758db3141d1541b0c66368b3a47b179c11f25d',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q3 (12-08_pm.pdf)
    (
        'Who among the following was the founder of All India Muslim League?',
        'Sir Syed Ahmad Khan',
        'Sir Mohammad Iqbal',
        'Agha Khan',
        'Nawab Salimullah Khan',
        NULL,
        '',
        '',
        'en',
        3,
        '4e7a31e377282b4025b531cf6f063d4ebc577025f46c1398920ca69036663036',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q4 (12-08_pm.pdf)
    (
        'The founder of Muslim League was',
        'Liaquat Ali',
        'Shaukat Ali',
        'Nawab Salimullah',
        'M.A. Jinnah',
        NULL,
        '',
        '',
        'en',
        4,
        '562e9515c62ed2e08a48fe83dc939f87a3031665a0a19a7a1c8ed7b9612255ef',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q5 (12-08_pm.pdf)
    (
        'Who was the first President of the Muslim League?',
        'Agha Khan',
        'Hamid Khan',
        'Hasan Khan',
        'M.A. Jinnah',
        NULL,
        '',
        '',
        'en',
        5,
        '87a2fe52131a4d15995575f4ac877785876f26cb8b77086ee4ee010358567a3c',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q6 (12-08_pm.pdf)
    (
        'The annual session of Muslim League in the year 1907 was held at',
        'Dhaka',
        'Karachi',
        'Aligarh',
        'Lucknow',
        NULL,
        '',
        '',
        'en',
        6,
        '6edcd11fe2b2fc96c7586ebcb9b407a53712056960137103bd6badddedd691b0',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q7 (12-08_pm.pdf)
    (
        'With reference to the Indian freedom struggle, which one of the following statements is not correct?',
        'Hakim Ajmal Khan was one of the leaders to start a nationalist and militant Ahrar movement',
        'When the Indian National Congress was formed, Syed Ahmad Khan opposed it',
        'The All India Muslim League which was formed in 1906 vehemently opposed the partition of Bengal and separate electorates',
        'Maulana Barkat Ullah and Maulana Obeidullah Sindhi were among those who formed a Provisional Government of India in Kabul',
        NULL,
        '',
        '',
        'en',
        7,
        'f196c3c0100ef26485a6b17a6eed085e8ab534c2fb1b134a09cd18fc6b769c1b',
        'needs_review',
        now(),
        now()
    ),
    -- Ch13 Q8 (12-08_pm.pdf)
    (
        'The Muslim deputation met Minto in 1906 at Shimla and pleaded for',
        'Separate electorate for Muslims',
        'A composite electorate',
        'Higher representation to the Hindus',
        'Special representation to Muslim by nomination',
        NULL,
        '',
        '',
        'en',
        8,
        '03c7936c066737b77871ed3cb590291d71ea5ef8ab4619b912a85ccab58b8db7',
        'needs_review',
        now(),
        now()
    ),
    -- Ch16 Q9 (12-10_pm.pdf)
    (
        'Which implication was taken in Lucknow session of Congress in 1916?',
        'Separate electorate demand of Muslim League was accepted',
        'Temporary merger of Muslim League and Congress occurred',
        'A Muslim person was elected as President of Congress',
        'None of the above',
        'A',
        '',
        '',
        'en',
        9,
        'fbb65ad9e8c0908d00dc24f3d67846872752fc6d06aa0f223db484f9bc15de47',
        'needs_review',
        now(),
        now()
    ),
    -- Ch16 Q10 (12-10_pm.pdf)
    (
        'The Congress for the first time accepted the system of separate electorate for Muslims in the year',
        '1909',
        '1916',
        '1931',
        '1932',
        'B',
        '',
        '',
        'en',
        10,
        'b6d7517495f265d9883ad7857681106b8b49febf34ba286880bb7e5ac2b9e358',
        'needs_review',
        now(),
        now()
    ),
    -- Ch16 Q11 (12-10_pm.pdf)
    (
        'Which one of the following is not correct about the Congress Session of Lucknow, 1916?',
        'Ambika Charan Majumdar was not the President of this session',
        'In this session, the reunion between the liberal and the extremist was established',
        'Mahatma Gandhi was apprised of the problems of the peasants of Champaran for the first time',
        'None of the above',
        'A',
        '',
        '',
        'en',
        11,
        '165230174bcecf6f5820e28493a79df0a82161393643a393f2d4e7d5da772cf6',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q1 (12-10_pm.pdf)
    (
        'Who founded a branch of ''HOME-RULE League'' at Dehradun in 1918?',
        'Swami Satyadeva',
        'Swami Dayanand Saraswati',
        'Swami Vicharanand Saraswati',
        'Tara Dutt Gairola',
        'C',
        '',
        '',
        'en',
        1,
        '1a9d65f2a5660bd04ed15ab66f51c70a7ff72e77500efe0a45253997e38afa11',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q2 (12-10_pm.pdf)
    (
        'Consider the statements regarding the Home Rule League.
1. S. Subramaniya Ayer was an associate of Annie Besant.
2. It started on behalf of the Indian National Congress.
3. It changed its name to Swarajya sabha.
4. Its flag had the Union Flag on it.
Which of the following are correct?',
        '1, 2 and 3',
        '2, 3 and 4',
        '1, 3 and 4',
        'Only 1 and 2',
        'C',
        '',
        '',
        'en',
        2,
        'ee08a0d5968ef5e837977de6540be7dd9f37d5a172ba1421b3ea18a831f7169e',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q3 (12-10_pm.pdf)
    (
        'Bal Gangadhar Tilak was given the epithet of ''Lokmanya'' (Universally Respected) during',
        'Swadeshi movement',
        'Revolutionary movement',
        'Home Rule movement',
        'His imprisonment in 1908',
        'C',
        '',
        '',
        'en',
        3,
        '12b7df540da1005b97d57d7f561ef203640136891eea5fc1c3cab2a67d4fce39',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q4 (12-10_pm.pdf)
    (
        'Annie Besant is mostly associated with',
        'Civil Disobedience Movement',
        'Home Rule Movement',
        'Khilafat Movement',
        'Non-Co-operation Movement',
        'B',
        '',
        '',
        'en',
        4,
        'aa65bb480cd312e457927c5747919b29301dcc199d68493db4f67ebc728ed254',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q5 (12-10_pm.pdf)
    (
        'The movement in India which became popular during the first World War was the',
        'Swadeshi and Boycott Movement',
        'Home Rule Movement',
        'Separatist Movement',
        'Swaraj Party Movement',
        'B',
        '',
        '',
        'en',
        5,
        'f4b512e1fdca9306b21cfeb1c4cb2377d9dbe67d7180a6847fe725029e1c6701',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q6 (12-10_pm.pdf)
    (
        'Who launched the first Home Rule League Movement?',
        'Annie Besant',
        'Sarojini Naidu',
        'Surendra Nath Banerjee',
        'Tilak',
        'D',
        '',
        '',
        'en',
        6,
        '4639493dfcde37231260773e869f45e2bdffe2de8d54010f7583ada29d00a8fe',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q7 (12-10_pm.pdf)
    (
        'Two Home Rule Leagues were started in 1915-16 under the leadership of',
        'Tilak and Annie Besant',
        'Tilak and Aurobindo Ghosh',
        'Tilak and Lala Lajpat Rai',
        'Tilak and Vipin Chandra Pal',
        'A',
        '',
        '',
        'en',
        7,
        '286b30d68be9e1dee202ca0ce0764d2eaf211d667e9b6e123e17521b7cacb0d6',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q8 (12-10_pm.pdf)
    (
        'Who among the following did not contribute to Home Rule League?',
        'Bal Gangadhar Tilak',
        'Annie Besant',
        'S. Subramaniam Iyer',
        'T.S. Alcott',
        'D',
        '',
        '',
        'en',
        8,
        '936cc9aaf68d0c7bba28aef068907c0a586a5a74f3387429a5144ddfdbafa246',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q9 (12-10_pm.pdf)
    (
        'Which of the following is not associated with Home Rule Movement?',
        'C.R. Das',
        'S. Subramaniam Iyer',
        'Annie Besant',
        'B.G. Tilak',
        'A',
        '',
        '',
        'en',
        9,
        '503461e6ba612819c94bf8c97449d70addb05053aa30001a220c3371792f3726',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q10 (12-10_pm.pdf)
    (
        'The Home Rule Leagues of Tilak and Annie Besant were merged into one in',
        '1916',
        '1918',
        '1920',
        '1923',
        'B',
        '',
        '',
        'en',
        10,
        '52093bd4b5a2093c5b876741de98f11cb18415f72b55de72b46d145d0d46c1a9',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q11 (12-10_pm.pdf)
    (
        'Which of the following is not correct about the Home Rule League?',
        'The plan was first presented in 1914-15 by Annie Besant',
        'The Home Rule League of Tilak was confined to Maharashtra, Karnataka, Central Provinces and Berar',
        'The Home Rule League founded by Tilak was much stronger',
        'Despite the differences between Tilak and Besant, both the Leagues continued to exist',
        'D',
        '',
        '',
        'en',
        11,
        '1c6c84b10b9ceae6449b8b61c6aeb1181622ed400343b8a557d404505bbbdc60',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q12 (12-10_pm.pdf)
    (
        'Who among the following was a proponent of Fabianism as a movement?',
        'Annie Besant',
        'A.O. Hume',
        'Michael Madhusudan Dutt',
        'D.R. Palme Dot',
        'A',
        '',
        '',
        'en',
        12,
        'a23e04b9f324048f77b5631e397483b06a583cbb11c6127c4fb18f5d7e0d3d8f',
        'needs_review',
        now(),
        now()
    ),
    -- Ch17 Q13 (12-10_pm.pdf)
    (
        'Annie Besant was
1. responsible for starting the Home Rule Movement.
2. the founder of the Theosophical Society.
3. once the President of the Indian National Congress.
Select the correct answer using the code given below.',
        'Only 1',
        'Only 2 and 3',
        'Only 1 and 3',
        'All of the above',
        'C',
        '',
        '',
        'en',
        13,
        'd98d1c593f8a48e62cc9aefc1421369a1c6f43ca75d8a32f621004993c0f6b4a',
        'needs_review',
        now(),
        now()
    ),
    -- Ch18 Q1 (12-10_pm.pdf)
    (
        'In 1918, at which place Badridutt Pandey met with Mahatma Gandhi and informed him about the Coolie-Begar System?',
        'Delhi',
        'Calcutta',
        'Lucknow',
        'Bombay',
        NULL,
        '',
        '',
        'en',
        1,
        'd61ed870961f23dd4a4b3d5d2bd41042c387e6ca613e77f6667ae09f91a1812c',
        'needs_review',
        now(),
        now()
    ),
    -- Ch18 Q2 (12-10_pm.pdf)
    (
        'The political strategy Struggle - Truce - Struggle or S-T-S came into prominence with a call for',
        'Swadeshi Movement',
        'Quit India',
        'Boycott of Simon Commission',
        'Khilafat issue',
        NULL,
        '',
        '',
        'en',
        2,
        'a593206f90b5727cbd41fec1ffb78c0f7422a443fb88f6dc0e4fc8150393e1bf',
        'needs_review',
        now(),
        now()
    ),
    -- Ch18 Q3 (12-10_pm.pdf)
    (
        'When Mahatma Gandhi declared "Father of the Nation"',
        '20th July 1946',
        '12th August 1947',
        '15th March 1948',
        'Never, officially',
        NULL,
        '',
        '',
        'en',
        3,
        'd91d8c4cd20b602060a4fd4153b89de533e43e1873a51338181363153d2af985',
        'needs_review',
        now(),
        now()
    ),
    -- Ch18 Q4 (12-10_pm.pdf)
    (
        'At the end of the Civil Disobedience Movement Gandhiji took out a padyatra against untouchability. His first padyatra was undertaken in 1934 in',
        'Nagpur',
        'Noakhali',
        'Jharsuguda',
        'Thanjavur',
        NULL,
        '',
        '',
        'en',
        4,
        '83e9e0b4aa258b598e79550228ae36176771adc2cf02a9e033b28468a0711d1a',
        'needs_review',
        now(),
        now()
    ),
    -- Ch18 Q5 (12-10_pm.pdf)
    (
        'The cook from Bihar who saved Mahatma Gandhi''s life from a murder attempt by food poisoning in 1917 was',
        'Muzaffar Ahmad',
        'Batak Mian',
        'Mir Bakawal',
        'None of them',
        NULL,
        '',
        '',
        'en',
        5,
        '62bfa5472537c1c3abc66c62203e5662f1e29e509f030417d97a86f7549cf446',
        'needs_review',
        now(),
        now()
    ) ON CONFLICT (content_hash) DO NOTHING;
INSERT INTO bank_previousyearref (question_id, exam_name, year)
SELECT q.id,
    v.exam_name,
    v.year
FROM (
        VALUES (
                '8afdac07869e35040eef835634d3a1c3ce913bdb059a6929325d08eac6162495',
                'UPRO/ARO (Mains)',
                2013
            ),
            (
                '87adb0daddc9388a20d0a026c2aee807656288e842103aa726b5dbeeef4f74f6',
                '60th to 62nd BPSC (Pre)',
                2016
            ),
            (
                'd3ff8904048147a9d60460ac5de7fd977869fd35cf8deed2a485ea2a4cf20b21',
                'Uttarakhand UDA/LDA (Pre)',
                2007
            ),
            (
                'aacffd649ed8904481403041dc32b9b3e21dde1f3f562c7e378a9d4b2fae3d1b',
                'UPRO/ARO (Pre)',
                2014
            ),
            (
                '20952cc910ebca85c7c0019d728a2b3fdae0001c3bc19535cc137bfbedc7f40c',
                'UP Lower Sub. (Pre)',
                2008
            ),
            (
                '7c9647ed4b11f88974216717b88230d96727d2335cbecc53b61fb016e692f797',
                'UPPCS (Pre)',
                2014
            ),
            (
                '346fc77deaed8be6c96aabe9b8685c036759054686b2bff38fe0269b94f9730d',
                'UPPCS (Pre)',
                1990
            ),
            (
                'c9d895ac85f356dd2d21b492aaa7923021d66a01f19bbe75a2b5cb2a6b66811e',
                'Andhra Pradesh PSC (Pre)',
                2019
            ),
            (
                'c9d895ac85f356dd2d21b492aaa7923021d66a01f19bbe75a2b5cb2a6b66811e',
                'UPPCS (Mains)',
                2012
            ),
            (
                'f0edb79d71bf28a187b57758e76726e036001724e73640be3c9d81ebd42b268c',
                'UP UDA/LDA (Pre)',
                2010
            ),
            (
                'f0edb79d71bf28a187b57758e76726e036001724e73640be3c9d81ebd42b268c',
                'UPPCS (Mains)',
                2007
            ),
            (
                '7366e72b3e109080c21309155fdfbec4bf409a9ad805ddc29cdfb5f84ff5ce65',
                'IAS (Pre)',
                2010
            ),
            (
                'f01c9ee746ee6a4d7f39fb761bd370e57af9292db804a5b258b221250d78fce0',
                '56th to 59th BPSC (Pre)',
                2015
            ),
            (
                'e806cadde0750a616afdd840efaaa76edbd90d754ac3437066b860cb6ff468b1',
                'Uttarakhand UDA/LDA (Pre)',
                2003
            ),
            (
                'c775e4cfdd234e768a38c535b65a082d260ac49f73e6be9c9263156d035fe8fb',
                'Uttarakhand PCS (Mains)',
                2002
            ),
            (
                'af32882ec3f54122db6f3b63b0af332be2b8c9685341b408da0c3543e6d39055',
                'IAS (Pre)',
                2016
            ),
            (
                '2dae38d8ff176124eba24197ccf0bed0394db70c0a2ff24d84fef723f3e12599',
                'MPPCS (Pre)',
                1992
            ),
            (
                '2dae38d8ff176124eba24197ccf0bed0394db70c0a2ff24d84fef723f3e12599',
                'Uttarakhand UDA/LDA (Pre)',
                2007
            ),
            (
                'c9f86fd050a3ed2b0a2c58878a758db3141d1541b0c66368b3a47b179c11f25d',
                'MPPCS (Pre)',
                2014
            ),
            (
                '4e7a31e377282b4025b531cf6f063d4ebc577025f46c1398920ca69036663036',
                'UPPCS (Pre)',
                2007
            ),
            (
                '4e7a31e377282b4025b531cf6f063d4ebc577025f46c1398920ca69036663036',
                '41st BPSC (Pre)',
                1996
            ),
            (
                '562e9515c62ed2e08a48fe83dc939f87a3031665a0a19a7a1c8ed7b9612255ef',
                'UPPCS (Mains)',
                2006
            ),
            (
                '87a2fe52131a4d15995575f4ac877785876f26cb8b77086ee4ee010358567a3c',
                'UPPCS (Pre)',
                1997
            ),
            (
                '87a2fe52131a4d15995575f4ac877785876f26cb8b77086ee4ee010358567a3c',
                'Chhattisgarh PCS (Pre)',
                2015
            ),
            (
                '6edcd11fe2b2fc96c7586ebcb9b407a53712056960137103bd6badddedd691b0',
                'UP Lower Sub. (Pre)',
                2008
            ),
            (
                'f196c3c0100ef26485a6b17a6eed085e8ab534c2fb1b134a09cd18fc6b769c1b',
                'IAS (Pre)',
                2002
            ),
            (
                '03c7936c066737b77871ed3cb590291d71ea5ef8ab4619b912a85ccab58b8db7',
                '46th BPSC (Pre)',
                2004
            ),
            (
                'fbb65ad9e8c0908d00dc24f3d67846872752fc6d06aa0f223db484f9bc15de47',
                'Mizoram PSC (Pre)',
                2018
            ),
            (
                'b6d7517495f265d9883ad7857681106b8b49febf34ba286880bb7e5ac2b9e358',
                'RAS/RTS (Pre)',
                1999
            ),
            (
                '165230174bcecf6f5820e28493a79df0a82161393643a393f2d4e7d5da772cf6',
                'UPPCS (GIC)',
                2010
            ),
            (
                '1a9d65f2a5660bd04ed15ab66f51c70a7ff72e77500efe0a45253997e38afa11',
                'Uttarakhand PCS (Pre)',
                2025
            ),
            (
                'ee08a0d5968ef5e837977de6540be7dd9f37d5a172ba1421b3ea18a831f7169e',
                'Odisha PSC (Pre)',
                2023
            ),
            (
                '12b7df540da1005b97d57d7f561ef203640136891eea5fc1c3cab2a67d4fce39',
                'West Bengal PSC (Pre)',
                2023
            ),
            (
                'aa65bb480cd312e457927c5747919b29301dcc199d68493db4f67ebc728ed254',
                'UPPCS (Mains)',
                2010
            ),
            (
                'f4b512e1fdca9306b21cfeb1c4cb2377d9dbe67d7180a6847fe725029e1c6701',
                'UP Lower Sub. (Pre)',
                2008
            ),
            (
                '4639493dfcde37231260773e869f45e2bdffe2de8d54010f7583ada29d00a8fe',
                'UPPCS (Pre)',
                1993
            ),
            (
                '4639493dfcde37231260773e869f45e2bdffe2de8d54010f7583ada29d00a8fe',
                'UPPCS (Pre)',
                1991
            ),
            (
                '286b30d68be9e1dee202ca0ce0764d2eaf211d667e9b6e123e17521b7cacb0d6',
                'UP UDA/LDA (Pre)',
                2001
            ),
            (
                '936cc9aaf68d0c7bba28aef068907c0a586a5a74f3387429a5144ddfdbafa246',
                '40th BPSC (Pre)',
                1995
            ),
            (
                '503461e6ba612819c94bf8c97449d70addb05053aa30001a220c3371792f3726',
                'UPPCS (Pre)',
                2010
            ),
            (
                '52093bd4b5a2093c5b876741de98f11cb18415f72b55de72b46d145d0d46c1a9',
                'UPPCS (Mains)',
                2002
            ),
            (
                '1c6c84b10b9ceae6449b8b61c6aeb1181622ed400343b8a557d404505bbbdc60',
                'UPPCS (Pre)',
                2004
            ),
            (
                'a23e04b9f324048f77b5631e397483b06a583cbb11c6127c4fb18f5d7e0d3d8f',
                'IAS (Pre)',
                2005
            ),
            (
                'd98d1c593f8a48e62cc9aefc1421369a1c6f43ca75d8a32f621004993c0f6b4a',
                'IAS (Pre)',
                2013
            ),
            (
                'd61ed870961f23dd4a4b3d5d2bd41042c387e6ca613e77f6667ae09f91a1812c',
                'Uttarakhand PCS (Pre)',
                2025
            ),
            (
                'a593206f90b5727cbd41fec1ffb78c0f7422a443fb88f6dc0e4fc8150393e1bf',
                '70th BPSC (Pre)',
                2024
            ),
            (
                'd91d8c4cd20b602060a4fd4153b89de533e43e1873a51338181363153d2af985',
                'Odisha PSC (Pre)',
                2024
            ),
            (
                '83e9e0b4aa258b598e79550228ae36176771adc2cf02a9e033b28468a0711d1a',
                'Odisha PSC (Pre)',
                2024
            ),
            (
                '62bfa5472537c1c3abc66c62203e5662f1e29e509f030417d97a86f7549cf446',
                '69th BPSC (Pre)',
                2023
            )
    ) AS v(content_hash, exam_name, year)
    JOIN bank_question q ON q.content_hash = v.content_hash ON CONFLICT DO NOTHING;
COMMIT;