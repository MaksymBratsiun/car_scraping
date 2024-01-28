PGDMP                          |            cars    15.2 (Debian 15.2-1.pgdg110+1)    15.2 (Debian 15.2-1.pgdg110+1)                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            	           1262    20225    cars    DATABASE     o   CREATE DATABASE cars WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE cars;
                postgres    false            �            1259    20253    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    20243    offers    TABLE     �  CREATE TABLE public.offers (
    id integer NOT NULL,
    url character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    price_usd integer,
    odometer integer,
    username character varying(63),
    phone_number character varying(31) NOT NULL,
    image_url character varying(255),
    images_count integer,
    car_number character varying(12),
    car_vin character varying(17),
    datetime_found date NOT NULL
);
    DROP TABLE public.offers;
       public         heap    postgres    false            �            1259    20242    offers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.offers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.offers_id_seq;
       public          postgres    false    215            
           0    0    offers_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.offers_id_seq OWNED BY public.offers.id;
          public          postgres    false    214            l           2604    20246 	   offers id    DEFAULT     f   ALTER TABLE ONLY public.offers ALTER COLUMN id SET DEFAULT nextval('public.offers_id_seq'::regclass);
 8   ALTER TABLE public.offers ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215                      0    20253    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    216                      0    20243    offers 
   TABLE DATA           �   COPY public.offers (id, url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found) FROM stdin;
    public          postgres    false    215                       0    0    offers_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.offers_id_seq', 96, true);
          public          postgres    false    214            r           2606    20257 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    216            n           2606    20250    offers offers_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.offers DROP CONSTRAINT offers_pkey;
       public            postgres    false    215            p           2606    20252    offers offers_url_key 
   CONSTRAINT     O   ALTER TABLE ONLY public.offers
    ADD CONSTRAINT offers_url_key UNIQUE (url);
 ?   ALTER TABLE ONLY public.offers DROP CONSTRAINT offers_url_key;
       public            postgres    false    215                  x�KI1�4I22K167����� ,��         C	  x��YKS�^7��R�B������ S��Ƞ1�AMI���g&�,�H2S3SSy�d�MR�m*;�7��Qν݂n��f��}��w�w����Rx�ax4���{��0X�wۋ�����g������u��N�?8�w{a��3����.^=9T(�!��B�M0����mt>C�@���K,կ�p8,�A����b����h?�A���E�xoW!�/��\q�?[����������N�ۮ�D�m�9�Ŕ0)P� ��D�������7�H*b�U� u�6	 ������ݬ�պ��Yxi����cF0*T����[ՍM��j���<�Q�����?g��_���Z�^�򸰰��_�o���<z?z�����}�FG�F?E��7��P�#��l�%<8�olؔ$�<IH�p̹R,I �M$8�h�艇��-��[Xia2�93 ��cz_f@vcoW)��b?�*#ҨN�{� =���q������Ed�6�Z�K�ڦ$���Qd���"():��0!2�.*������������e�䜌�GE��,0[�׹Q��)�V��I`�[H��d����Yj��wC+�!�4��v���5Z��Z��@�e�����r�����}�*�����G?Y��.�� %�A��n��%D�\�o�;ZnKHs �[7���n�1 :��������n�L
�5I�q|���ުPoJ�L�Wl��{� �=����~���M��8���6�j�!TN�r jsE�wo/�
6��EX@aj�62)Oh�)iXn��x���Oj������� �'��'�6�W�2���M���� 56��]�r��� ��c�	E?�� �x=�
���ч��߆����P�����R��Z�z�ziyI�U�f�f�0��O��O:=���s��x��R�T����RY�l�$TP�f� ��U��8(`�7A#$t�	���JfIʆ��dP��$�1Ba�<��A��	8��v��{�MH'q"��z � 	�j�s6���RD��1:�1:���I�\�b+$���l>�m"2·V^����޷T�V�K�v�����$d�k:l�|*}.�m��n���5D�"<�EA=���-��|����s���)��v���P
6�앦�5K��z�J��ΐmÇe����H@����Jlo�J���O�*K�e�%�Q�={7z	����ܒ���^�����hW��Z����h�sS�xh��p�,�9V+UXap��w����D�7���x��b�����,z;��ݴ�����@Ԯi��[�;;;卝Z���Ʈs�1�C�ta�U#Mɥ����R�i��?��e�eXrau_H>�lqr���Ԗ��Z�Z˪;a�&��2����������E���UU# Q�{u@��vt�����YW��0L%}�0�XF����X��5A�d��R,{�s<�u|�I��Y|�0»�g\ȩ���e<�h;_q![�L0Z5����ZLg��1rS�!���nk\���9�>�ڳLo��ĸ�e �[�����z�W0�Ze�F=Ǿ]�g�U�k����c�gb��v3��,��f�������{��8̔*���9h���(j�l��V��V�[]�^���� �a���v�@�����#�\Y��@+���մ�5`f�pND`m�1S����)�	+�tc��3Xs�җ̥���Kf����i�B��0Ur����;�gN�����b�N�U]'%Rx�t[�1v�����˛��b�����/�N�@�x�& ��M�u*)S_��mZ��(��F{�%Dgh�qQ�tj��̬����vx�$:��Db�����(�=?�z��*>l�[{*��Ǒ�j�4���E+�\�5��&������ZP0���k�e�yr(�ѫ�fU���fo-s����-�^>. �'W����-�K��௬�������#~FM7sqFn1R�3���Эi�	5Svړ�[s��r���v����n>���9�.��pX[w+������v��K&�eW��s����mM_��J�{�kW��"��3I�S�G�2l��6 Mn~""��A~k�,�o��(я΋}���Ss��l8�:3�X�h*���e���`��̵�T2�T�4F�UR�e�v#F�B?�`H��0���%�R�$�ߤ���n�l�G]U�xo�W�������a�J�-�u��v+��{�ֶ�ǑҲGx&s��S ��(���N����:�u��<�G�6����N�w:��eb�X�1K>���ov�G�eM����B5"�7��C��     