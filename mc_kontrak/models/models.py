# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import is_html_empty
from dateutil.relativedelta import relativedelta


class mc_kontrak(models.Model):
    _name = 'mc_kontrak.mc_kontrak'
    _description = 'Custom module untuk data kontrak'

    # Field
    name = fields.Char(string='No Kontrak', readonly=True, default='New')
    mc_cust = fields.Many2one('res.partner', string='Customer', domain=[("is_company", '=', True)])
    mc_pic_cust = fields.Char(string='PIC Customer')
    mc_create_date = fields.Date(string='Created Date', readonly=True, store=True, default=fields.Datetime.now())
    mc_confirm_date = fields.Date(string='Confirm Date', readonly=True, copy=False)
    mc_total = fields.Monetary(string='Total', readonly=True, compute='total_harga', store=True)
    mc_pajak = fields.Monetary(string='Total Pajak', readonly=True, store=True)
    mc_tak_pajak = fields.Monetary(string='Total Tak Pajak', readonly=True, store=True)
    mc_isopen = fields.Boolean(default=True)
    mc_sales = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    mc_admin_sales = fields.Many2one('res.users', string='Admin Sales', default=lambda self: self.env.user,
                                     readonly=True)

    x_subtotal_otf = fields.Monetary(string='Subtotal One Time Fee')
    x_subtotal_sub = fields.Monetary(string='Subtotal Subscription')
    mc_qty_kontrak = fields.Integer(default=0, store=True)

    x_kontrak_start_date = fields.Date(string="Kontrak Start Date")
    x_kontrak_end_date = fields.Date(string="Kontrak End Date")
    x_note = fields.Html(store=True, default='<center> <h2>PERJANJIAN KERJA SAMA</h2> <span>No.</span> <span t-field="doc.name"></span> </center> <br/> <p> Perjanjian kerja sama ini (<b>"Perjanjian"</b>), dibuat dan ditandatangani pada hari ini tanggal (<b>"Tanggal Efektif"</b>) oleh dan antara: </p><p> 1. <b>PT. OTTO MENARA GLOBALINDO</b>, suatu perseroan terbatas yang didirikan berdasarkan dan tunduk pada hukum negara Republik Indonesia, yang memiliki alamat terdaftar di Jl. Rungkut Tengah No. 74, RT. 003, RW. 003, Rungkut Tengah, Gunung Anyar, Kota Surabaya, Jawa Timur, dalam hal ini diwakili secara sah oleh <b>Andi Setiadi</b>, dalam kapasitasnya sebagai Direktur, selanjutnya disebut sebagai <b>"PIHAK PERTAMA"</b>; dan </p><p> 2. <b> <span t-field="doc.mc_cust.name"></span> </b> , suatu perseroan terbatas yang didirikan berdasarkan dan tunduk pada hukum negara Republik Indonesia, yang memiliki alamat terdaftar di <span t-field="doc.mc_cust.street"></span> <span t-field="doc.mc_cust.street2"></span> <span t-field="doc.mc_cust.city"></span>, dalam hal ini diwakili secara sah oleh <span t-field="doc.mc_pic_cust"></span> , dalam kapasitasnya sebagai Direktur, bertindak untuk dan atas nama selanjutnya disebut sebagai <b>"PIHAK KEDUA"</b>. </p><br/> <p> PIHAK PERTAMA dan PIHAK KEDUA, masing-masing disebut sebagai <b>"PIHAK"</b> dan secara bersama-sama disebut sebagai <b>"PARA PIHAK"</b>. </p><br/> <center> <p> <b>Pasal 1<br/>RUANG LINGKUP </b> </p></center> <p> <ol> <li> PIHAK PERTAMA adalah pemilik produk berupa alat pelacak lokasi digital berikut dengan komponen-komponen pendukungnya (termasuk antara lain namun tidak terbatas sensor suhu, pintu, bahan bakar, dll) (<b>"Produk Hardware"</b>) dan perangkat lunak pelacak lokasi (<b> "Produk Software"</b>) (Produk Hardware dan Produk Software selanjutnya disebut sebagai <b> "Produk"</b>). </li><li> PIHAK PERTAMA bermaksud untuk menawarkan Produk yang telah memenuhi spesifikasi yang telah disepakati secara tertulis sebelumnya oleh PIHAK KEDUA dalam suatu dokumen pesanan pembelian dalam bentuk dan isi pesanan pembelian sebagaimana terlampir dalam <b>Lampiran 1</b> Perjanjian ini. </li><li> Penawaran yang diberikan oleh PIHAK PERTAMA kepada PIHAK KEDUA dapat dilakukan melalui beberapa paket yakni melalui (i) pembelian Produk Hardware; (ii) pembelian Produk Hardware dan berlangganan Produk Software; (iii) berlangganan Produk Software; atau (iv) penyewaan Produk Hardware yang telah dilengkapi dengan Produk Software. Penawaran yang disepakati oleh PARA PIHAK dapat secara rinci dilihat dalam pesanan pembelian sebagaimana terlampir dalam <b> Lampiran 1 </b> Perjanjian ini. </li></ol> </p><p style="page-break-before:always;"></p><center> <p> <b>Pasal 2<br/>JANGKA WAKTU </b> </p></center> <p> <ol> <li> Perjanjian ini berlaku selama 12 (dua belas) bulan terhitung sejak tanggal sampai dengan tanggal (<b>"Jangka Waktu"</b>). </li><li> Jangka Waktu Perjanjian ini akan diperpanjang secara otomatis dengan masa perpanjangan 12 (dua belas) bulan. Tanggal perpanjangan atas Perjanjian akan diberitahukan secara tertulis oleh PIHAK PERTAMA kepada PIHAK KEDUA sebelum berakhirnya Jangka Waktu (<b>"Jangka Waktu Perpanjangan"</b>). Untuk menghindari keraguan, perpanjangan jangka waktu dari Perjanjian tidak memerlukan suatu perjanjian terpisah yang dibuat secara tertulis di antara PARA PIHAK. </li></ol> </p><br/> <center> <p> <b>Pasal 3<br/>HARGA DAN PEMBAYARAN </b> </p></center> <p> <ol> <li> Jenis dan harga Produk yang disepakati, dapat dilihat lebih rinci dalam <b>Lampiran 1 </b> Perjanjian ini. </li><li> Tata cara dan termin pembayaran diatur lebih rinci dalam <b>Lampiran 2</b> Perjanjian ini. </li><li> Apabila pembayaran dimuka secara penuh telah dilakukan kepada PIHAK PERTAMA oleh PIHAK KEDUA, dan selanjutnya PIHAK KEDUA berniat untuk mengakhiri Perjanjian ini, maka PIHAK KEDUA setuju bahwa pembayaran dimuka secara penuh yang telah dilakukan akan diperhitungkan sebagai kompensasi ganti kerugian untuk PIHAK PERTAMA, dengan ketentuan pembayaran dimuka secara penuh tersebut telah dilakukan untuk keseluruhan Jangka Waktu ataupun keseluruhan Jangka Waktu Perpanjangan yang sedang berjalan. </li><li> Pajak-pajak yang timbul sehubungan dengan Perjanjian ini akan menjadi tanggung jawab dari masing-masing Pihak sesuai dengan peraturan perpajakan yang berlaku di Republik Indonesia. </li><li> Apabila tanggal jatuh tempo pembayaran jatuh pada hari libur (termasuk hari Sabtu dan Minggu di Indonesia) atau hari libur Nasional yang ditetapkan oleh pemerintah Indonesia, maka pembayaran harus dilakukan pada hari kerja sebelumnya. </li><li> Apabila terjadi pembayaran melewati tanggal jatuh tempo, PIHAK PERTAMA berhak untuk menghentikan penyediaan dan/atau penyewaan Produk Hardware dan/atau layanan langganan Produk Software kepada PIHAK KEDUA, dengan tidak mengurangi kewajiban pelunasan pembayaran oleh PIHAK KEDUA. </li><li> Pembayaran yang dilakukan oleh PIHAK KEDUA kepada PIHAK PERTAMA dilakukan hanya melalui nomor rekening sebagaimana tercantum dalam pesanan pembelian sebagaimana terlampir dalam <b>Lampiran 2</b> Perjanjian ini. Segala bentuk pembayaran yang dilakukan oleh PIHAK KEDUA ke nomor rekening selain nomor rekening PIHAK PERTAMA yang tercantum dalam pesanan pembelian sebagaimana terlampir dalam <b>Lampiran 2</b> Perjanjian ini bukan merupakan tanggung jawab PIHAK PERTAMA. </li></ol> </p><p style="page-break-before:always;"></p><center> <p> <b>Pasal 4<br/>HAK DAN KEWAJIBAN PARA PIHAK </b> </p></center> <p> <ol> <li> PIHAK PERTAMA wajib menyediakan Produk Hardware dan layanan berlangganan Produk Software kepada PIHAK KEDUA sesuai dengan tipe kerja sama yang dipilih oleh PIHAK KEDUA berdasarkan pesanan pembelian dalam Lampiran 1 Perjanjian ini. </li><li> PIHAK KEDUA yang memilih opsi Produk yang disebutkan dalam Pasal 1 ayat 3 (iv) wajib memelihara dan menjaga kondisi Produk untuk memastikan kinerja yang optimal dan bersedia mengganti kerugian apabila terjadi kerusakan yang diakibatkan oleh kesalahan yang disengaja oleh PIHAK KEDUA. </li><li> Apabila terjadi kerusakan dan/atau kehilangan pada Produk Hardware yang diakibatkan oleh kesalahan yang disengaja oleh PIHAK KEDUA, PIHAK KEDUA akan dibebankan biaya penggantian kerugian sebesar Rp. 1.000.000 (Satu juta rupiah) per unit atas kesepakatan dari PARA PIHAK. </li><li> PIHAK KEDUA setuju untuk memberikan izin pemasangan Produk Hardware dan/atau Produk Software kepada PIHAK PERTAMA, termasuk namun tidak terbatas pada pelaksanaan interface terhadap seluruh atau sebagian aset PIHAK KEDUA dan/atau pihak lainnya. </li><li> Selama Jangka Waktu atau Jangka Waktu Perpanjangan , PIHAK KEDUA tidak berhak untuk: <ol type="a"> <li> mensublisensikan, menyewakan, menjual, meminjamkan atau mendistribusikan Produk kepada pihak manapun dengan alasan apapun; </li><li> menggunakan Produk selain sebagaimana yang diatur dalam Perjanjian ini; </li><li> menyalin, menerjemahkan, membongkar, mengurai atau merekayasa ulang Produk, termasuk akan tetapi tidak terbatas pada membuat atau berusaha untuk membuat sandi sumber dari sandi Produk; </li><li> melakukan modifikasi atas Produk tanpa persetujuan tertulis dari PIHAK PERTAMA. </li></ol> </li><li> PIHAK KEDUA tidak diperbolehkan menggunakan Produk untuk maksud-maksud amoral, tindakan kriminal dan aktivitas ilegal yang tidak sesuai dengan peraturan perundangan yang berlaku di Indonesia. </li></ol> </p><br/> <center> <p> <b>Pasal 5<br/>PEMBATASAN TANGGUNG JAWAB </b> </p></center> <p> PIHAK KEDUA bersedia untuk melepaskan tanggung jawab PIHAK PERTAMA, afiliasi-afiliasi PIHAK PERTAMA beserta karyawannya terhadap segala kerugian, klaim, proses hukum, pengeluaran, kerusakan, kewajiban, atau biaya yang timbul akibat dari penggunaan Produk yang tidak sesuai dengan maksud dan tujuan penggunaan yang tertera pada pemesanan pembelian sebagaimana yang dilampirkan pada <b>Lampiran 1</b> Perjanjian ini dan ketentuan-ketentuan dalam Perjanjian ini </p><br/> <p style="page-break-before:always;"></p><center> <p> <b>Pasal 6<br/>PENGAKHIRAN PERJANJIAN </b> </p></center> <p> <ol> <li> PIHAK PERTAMA tidak dapat mengakhiri Perjanjian ini secara sepihak dan seketika tanpa adanya kesepakatan dari PARA PIHAK terkait alasan pengakhiran. </li><li> PIHAK KEDUA tidak dapat mengakhiri Perjanjian ini secara sepihak, namun PIHAK KEDUA dapat mengajukan pengakhiran Perjanjian ini kepada PIHAK PERTAMA dengan memberikan permohonan tertulis 30 (tiga puluh) hari kerja sebelumnya yang menyebutkan alasan pengakhiran Perjanjian kepada PIHAK PERTAMA. Atas permohonan pengakhiran Perjanjian ini oleh PIHAK KEDUA, PIHAK PERTAMA berhak mengenakan denda pengakhiran yang perhitungannya akan dilakukan oleh PIHAK PERTAMA dalam suatu surat terpisah yang akan dikirimkan kepada PIHAK KEDUA, dengan memperhitungkan sisa Jangka Waktu ataupun sisa Jangka Waktu Perpanjangan. </li><li> PIHAK KEDUA tidak dapat mengakhiri Perjanjian ini secara sepihak, namun PIHAK KEDUA dapat mengajukan pengakhiran Perjanjian ini kepada PIHAK PERTAMA dengan memberikan permohonan tertulis 30 (tiga puluh) hari kerja sebelumnya yang menyebutkan alasan pengakhiran Perjanjian kepada PIHAK PERTAMA. Atas permohonan pengakhiran Perjanjian ini oleh PIHAK KEDUA, PIHAK PERTAMA berhak mengenakan denda pengakhiran yang perhitungannya akan dilakukan oleh PIHAK PERTAMA dalam suatu surat terpisah yang akan dikirimkan kepada PIHAK KEDUA, dengan memperhitungkan sisa Jangka Waktu ataupun sisa Jangka Waktu Perpanjangan. </li><li> Sehubungan dengan pengakhiran Perjanjian ini, PARA PIHAK sepakat untuk mengesampingkan ketentuan yang terdapat dalam Pasal 1266 dan 1267 Kitab Undang-Undang Hukum Perdata sepanjang dibutuhkan persetujuan dari pengadilan untuk melakukan pengakhiran Perjanjian ini. Pengakhiran ini tidak akan melepaskan setiap Pihak dari segala kewajiban atau tanggung jawab Pihak tersebut dari segala hal yang disanggupi atau persyaratan yang belum dipenuhi, dikaji atau dilaksanakan oleh Pihak tersebut sebelum pengakhiran. </li><li> Perjanjian ini akan berakhir dengan sendirinya apabila salah satu pihak dinyatakan pailit, baik diwajibkan maupun secara sukarela, atau meminta penundaan pembayaran, atau terjadi pengalihan aset untuk kepentingan kreditur, atau mengalami kerugian atau eksekusi terhadap properti atau asetnya yang berbiaya atau secara keseluruhan. </li></ol> </p><br/> <p style="page-break-before:always;"></p><center> <p> <b>Pasal 7<br/>KERAHASIAAN </b> </p></center> <p> <ol> <li> PARA PIHAK sepakat untuk menghormati, menyimpan dan menjaga dengan sebaik-baiknya kerahasiaan dari setiap data, informasi, dokumen dan korespondensi dari masing-masing Pihak terkait dengan Perjanjian ini, termasuk dan tidak terbatas pada harga, fitur Produk dalam Perjanjian ini. </li><li> Kewajiban kerahasiaan tidak berlaku untuk informasi atau dokumen yang: <ol type="a"> <li> menjadi domain publik yang bukan dikarenakan pelanggaran; atau </li><li> harus diungkapkan kepada suatu otoritas pemerintahan, pengadilan, arbiter atau pengadilan administratif atau ahli dalam rangka proses persidangan atau penyelesaian sengketa sebelum pengungkapan tersebut. </li></ol> </li><li> Atas segala hal yang terkait dengan penggunaan Produk, PIHAK KEDUA memberikan persetujuan kepada PIHAK PERTAMA untuk: <ol type="a"> <li> memperoleh, mengakses, dan menyimpan data yang dimasukkan oleh PIHAK KEDUA ke dalam Produk dalam rangka penggunaan Produk secara optimal; </li><li> mengumpulkan informasi dari dan tentang PIHAK KEDUA, termasuk namun tidak terbatas pada nama orang, nama perusahaan, alamat surel, nomor telepon, dan informasi lainnya pada saat PIHAK KEDUA mengikatkan diri dalam Perjanjian ini; </li><li> menghapus segala data yang diunggah PIHAK KEDUA yang bertentangan dengan Perjanjian ini dan hukum yang berlaku di Indonesia; </li><li> memberikan data kepada pihak ketiga hanya apabila diperlukan, untuk melakukan aktivitas yang diperlukan dalam mengoptimalkan penggunaan Produk ; dan </li><li> mengirimkan pengumuman layanan, pesan administratif, dan informasi lainnya kepada PIHAK KEDUA. </li></ol> </li><li> PARA PIHAK harus melakukan semua langkah yang wajar sesuai dengan peraturan perundang-undangan yang berlaku di Indonesia untuk menjaga kerahasiaan segala data dan informasi, kecuali telah mendapatkan persetujuan tertulis dari salah satu Pihak. </li><li> Dalam hal perolehan, pengolahan/penggunaan, penyimpanan, penyebarluasan, dan pemusnahan data pribadi PIHAK KEDUA, PIHAK PERTAMA akan selalu mematuhi aturan dan ketentuan yang diatur dalam peraturan perundang-undangan yang berlaku mengenai perlindungan data pribadi. </li></ol> </p><center> <p> <b>Pasal 8<br/>WANPRESTASI </b> </p></center> <p> Apabila salah satu Pihak lalai atau gagal (<b>"Pihak Yang Melanggar"</b>) melaksanakan salah satu ketentuan yang ditetapkan dalam Perjanjian ini, maka Pihak Yang Melanggar tersebut dianggap telah melakukan wanprestasi (<b>"Wanprestasi"</b>) terhadap Pihak yang dilanggar hak-haknya (<b>"Pihak Yang Tidak Melanggar"</b>). Atas Wanprestasi tersebut, Pihak Yang Tidak Melanggar berhak untuk mengajukan pengakhiran Perjanjian secara sepihak sebelum habisnya Jangka Waktu atau Jangka Waktu Perpanjangan, tanpa dikenai denda atau kompensasi apa pun. </p><p style="page-break-before:always;"></p><center> <p> <b>Pasal 9<br/>KEADAAN KAHAR </b> </p></center> <p> <ol> <li> PARA PIHAK tidak bertanggung jawab dalam hal masing-masing pihak tidak dapat melakukan kewajibannya berdasarkan Perjanjian ini karena suatu peristiwa keadaan kahar, yaitu setiap kejadian yang terjadi diluar kekuasaan dan kendali Pihak tersebut, antara lain banjir, gempa bumi, kebakaran, tsunami, badai, angin topan, tanah longsor, bencana alam, teroris, kudeta, peperangan baik yang diumumkan atau tidak diumumkan, pemogokan massal, kebijakan dan tindakan Pemerintah Republik Indonesia terutama di bidang moneter dan fiskal, tindakan penguasa lainnya, huru-hara massal, kekacauan umum, tindakan militer, pemogokan, pemblokiran atau penutupan tempat-tempat kerja (lock-down), epidemi, pandemi dan kejadian lain-lain yang secara hukum dapat digolongkan kejadian dalam keadaan kahar untuk selanjutnya disebut sebagai <b>"Keadaan Kahar"</b>. </li><li> Pihak yang terkena Keadaan Kahar harus memberikan pemberitahuan tertulis kepada pihak lainnya mengenai Keadaan Kahar dalam jangka waktu 7 (tujuh) hari kalender dengan menyertakan analisis tentang perkiraan dampak dan lama waktu berlangsungnya Keadaan Kahar. Setelah pemberitahuan tersebut, seluruh kewajiban pihak yang terdampak Keadaan Kahar berdasarkan Perjanjian ini akan dengan segera tertunda, dan pihak tersebut harus melakukan segala tindakan semaksimal mungkin untuk melanjutkan kembali kinerja dengan sesegera mungkin. Keadaan Kahar ini harus didukung dengan bukti-bukti yang dan didukung dengan keterangan yang dibuat dan dikeluarkan oleh instansi yang berwenang </li><li> Ketika Keadaan Kahar berhenti, Perjanjian ini akan terus berlaku penuh selama Jangka Waktu atau Jangka Waktu Perpanjangan yang masih tersisa. </li><li> Apabila Keadaan Memaksa melampaui 3 (tiga) bulan, masing-masing Pihak berhak untuk mengakhiri Perjanjian tanpa ada tanggung jawab kepada Pihak yang lain. Pengakhiran tersebut tidak akan memberikan hak kepada Pihak manapun untuk mengklaim kerugian apapun. </li></ol> </p><br/> <center> <p> <b>Pasal 10<br/>HUKUM YANG BERLAKU DAN PENYELESAIAN PERSELISIHAN </b> </p></center> <p> <ol> <li> Perjanjian ini diatur oleh dan ditafsirkan berdasarkan hukum Negara Kesatuan Republik Indonesia. </li><li> PARA PIHAK sepakat apabila timbul sengketa dari atau sehubungan dengan Perjanjian ini, termasuk tapi tidak terbatas pada setiap sengketa mengenai keberadaan, keabsahan, pengakhiran hak atau kewajiban dari suatu Pihak (<b>"Sengketa"</b>), PARA PIHAK terlebih dahulu akan berupaya untuk menyelesaikan Sengketa tersebut dengan cara musyawarah untuk mufakat oleh PARA PIHAK yang didasarkan pada itikad baik dalam waktu 30 (tiga puluh) hari kalender sejak diterimanya suatu pemberitahuan tertulis mengenai adanya Sengketa oleh salah satu Pihak dari Pihak lainnya. </li><li> PARA PIHAK setuju bahwa setiap Sengketa yang tidak dapat diselesaikan secara musyawarah untuk mufakat dalam waktu 30 (tiga puluh) hari kalender sesuai dengan ketentuan Pasal 10 ayat 2 di atas, akan diselesaikan melalui Pengadilan Negeri Surabaya. </li></ol> </p><center> <p> <b>Pasal 11<br/>HAK ATAS KEKAYAAN INTELEKTUAL </b> </p></center> <p> <ol> <li> PIHAK KEDUA mengakui bahwa PIHAK PERTAMA adalah dan tetap menjadi pemilik dari seluruh kekayaan intelektual atas Produk, termasuk namun tidak terbatas pada hak cipta, hak atas bank data, hak merek, hak paten, dan rahasia dagang (<b>"HAKI"</b>). </li><li> Penggunaan Produk oleh PIHAK KEDUA bukan merupakan pengalihan kepemilikan atas HAKI maupun pengalihan kepemilikan atas hak lainnya yang melekat pada Produk kepada pihak manapun termasuk kepada PIHAK KEDUA. </li></ol> </p><p style="page-break-before:always;"></p><center> <p> <b>Pasal 12<br/>LAIN-LAIN </b> </p></center> <p> <ol> <li> <b>Lampiran.</b> Seluruh lampiran yang telah disepakati oleh PARA PIHAK dalam Perjanjian ini menjadi satu kesatuan yang tidak terpisahkan dari Perjanjian ini dan dalam pelaksanaannya tidak dapat berdiri sendiri. </li><li> <b>Adendum.</b> Setiap hal yang belum ditentukan atau disepakati oleh PARA PIHAK dalam Perjanjian ini dapat dibuat dan ditentukan di kemudian hari secara tertulis dan mengikat PARA PIHAK sebagai adendum dari Perjanjian ini. Adendum tersebut merupakan dokumen yang mempunyai kekuatan hukum yang sama dengan Perjanjian ini. </li><li> <b>Perubahan.</b> Masing-masing pihak dapat mengajukan usulan perubahan Perjanjian ini dengan memberikan usulan perubahan paling lambat 10 (sepuluh) hari kerja sebelum tanggal berlakunya perubahan. Perubahan terhadap Perjanjian ini hanya akan dibuat secara tertulis dengan persetujuan PARA PIHAK dan akan dianggap berlaku setelah perubahan tersebut ditandatangani oleh PARA PIHAK. </li><li> <b>Pengalihan.</b> PARA PIHAK tidak diperbolehkan untuk mengalihkan atau memindahtangankan seluruh atau sebagian dari hak atau kewajibannya dalam Perjanjian ini tanpa persetujuan tertulis dari Pihak lainnya. </li><li> <b>Keseluruhan Perjanjian.</b> Perjanjian ini termasuk setiap lampiran dan/atau perubahan dan/atau adendum yang terkait dengan Perjanjian ini merupakan suatu kesatuan, kesepakatan yang lengkap dari PARA PIHAK, bagian yang tidak terpisahkan dan merupakan pernyataan lengkap dan eksklusif mengenai ketentuan-ketentuan dari segala sesuatu yang disepakati oleh PARA PIHAK. Perjanjian ini menggantikan setiap dan seluruh perjanjian-perjanjian, nota kesepakatan, kesepakatan, dokumen-dokumen lainnya yang sebelumnya ditandatangani maupun kesepakatan lisan antara PARA PIHAK sehubungan dengan ruang lingkup Perjanjian ini, kecuali dokumen-dokumen sebelumnya yang dilampirkan dalam Perjanjian ini. </li><li> <b>Korespondensi.</b> Setiap pemberitahuan, persetujuan, pengesampingan dan komunikasi lain yang diberikan atau dibuat berdasarkan Perjanjian ini yang diperlukan atau diizinkan untuk diberikan oleh salah satu pihak berdasarkan Perjanjian ini harus dibuat dan disampaikan secara tertulis baik melalui surat pos maupun surat elektronik, serta ditandatangani oleh atau atas nama Pihak yang memberikan kepada Pihak lainnya. <br/> Korespondensi tersebut akan dianggap telah disampaikan apabila: <br/> <ol type="a"> <li>terdapat tanda terima saat diserahkan langsung kepada alamat yang bersangkutan; </li><li> dikirim melalui surel ke alamat surel PIHAK KEDUA yang tercantum dalam Perjanjian ini, dokumen asli yang bersangkutan harus tetap dikirimkan. </li></ol> Berikut adalah rincian korespondensi yang diakui dalam Perjanjian ini: <ul> <li> <b> <span t-field="doc.mc_sales.company_id.name"/> </b> <table border="0"> <tr> <td> Alamat </td><td>:</td><td> <span t-field="doc.mc_sales.company_id.partner_id.street"/> <span t-field="doc.mc_sales.company_id.partner_id.street"/>, <span t-field="doc.mc_sales.company_id.partner_id.city"/> </td></tr><tr> <td> Telepon </td><td>:</td><td>(031) 992 53933</td></tr><tr> <td> Surel </td><td>:</td><td>sales@mceasy.co.id</td></tr><tr> <td> Untuk Perhatian </td><td>:</td><td>Andi Setiadi (Direktur)</td></tr></table> </li><li> <b> <span t-field="doc.mc_cust.name"></span> </b> <table border="0"> <tr> <td> Alamat </td><td>:</td><td> <span t-field="doc.mc_cust.street"> <span t-field="doc.mc_cust.street2"> <span t-field="doc.mc_cust.city"></span> </span> </span> </td></tr><tr> <td> Telepon </td><td>:</td><td> <span t-field="doc.mc_cust.phone"></span> </td></tr><tr> <td> Surel </td><td>:</td><td> <span t-field="doc.mc_cust.email"></span> </td></tr><tr> <td> Untuk Perhatian </td><td>:</td><td> <span t-field="doc.mc_cust.name"></span> </td></tr></table> Apabila salah satu Pihak mengganti/mengubah informasi korespondensinya, maka Pihak yang bersangkutan harus memberitahukan kepada Pihak lainnya segera setelah adanya penggantian/perubahan tersebut kepada Pihak lainnya dengan cara apa pun. Perubahan akan dianggap efektif setelah 7 (tujuh) hari terhitung sejak tanggal diterimanya pemberitahuan perubahan tersebut. </li><li> <b>Tanda Tangan.</b> Perjanjian ini harus ditandatangani secara basah. Penandatanganan, pemindaian (scanned) dan/atau transmisi secara elektronik atas Perjanjian ini akan dianggap sebagai tanda tangan asli, dan tanda tangan yang dipindai (scanned) tersebut memiliki kekuatan hukum yang sama dengan tanda tangan asli, sepanjang tanda tangan tersebut dilakukan sesuai dengan ketentuan dan peraturan yang berlaku di Republik Indonesia. </li><li> <b>Rangkap.</b> Perjanjian ini juga dapat dibuat dan ditandatangani dalam beberapa rangkap, apabila dibuat dalam beberapa rangkap, masing-masing rangkap apabila digabungan akan membentuk satu perjanjian yang asli, utuh dan sah. </li></ul> Demikian PARA PIHAK telah sepakat dan Perjanjian ini ditandatangani oleh pejabat dari masing-masing Pihak yang secara sah dan berwenang pada hari, bulan dan tahun sebagaimana yang tertera pada bagian awal Perjanjian ini, dalam dua rangkap asli yang masing-masing bermeterai cukup dan berkekuatan hukum yang sama dan masing-masing diterima oleh setiap Pihak. </li></ol> </p><center> <table border="0" style="text-align: center; width:100%; table-layout:fixed;"> <tr> <td style="max-width:50%"> <b>PIHAK PERTAMA</b> </td><td style="max-width:50%"> <b>PIHAK KEDUA</b> </td></tr><tr> <td> <b>PT OTTO MENARA GLOBALINDO</b> </td><td> <b style="text-transform:uppercase"> <span t-field="doc.mc_cust.name"></span> </b> </td></tr><tr> <td height="150"></td><td height="150"></td></tr><tr> <td> <b> <u>Andi Setiadi</u> </b> </td><td> <b> <u> <span t-field="doc.mc_pic_cust"></span> </u> </b> </td></tr><tr> <td>Direktur</td><td>Direktur</td></tr></table> </center>')

    mc_state = fields.Selection([
        ('draft', 'Draft'),
        # ('sent', 'Quotation Sent'),
        ('done', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    so_count = fields.Integer(string='SO', compute='_count_so')
    subs_count = fields.Integer(string='Subscription', compute='_count_subs')

    # Relasi
    product_order_line = fields.One2many('mc_kontrak.product_order_line', 'kontrak_id', string='No Kontrak')
    histori_so_line = fields.One2many('mc_kontrak.histori_so', 'x_kontrak_id', string='Histori SO')
    currency_id = fields.Many2one('res.currency', default=12)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', domain=[("is_company", '=', True)], store=True)

    @api.onchange('x_kontrak_start_date')
    def get_one_year(self):
        if self.x_kontrak_start_date:
            self.x_kontrak_end_date = self.x_kontrak_start_date + relativedelta(years=1)

    @api.onchange('mc_cust')
    def change_pic_cust(self):
        self.mc_pic_cust = self.mc_cust.x_pic

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.mc_kontrak')
        vals_list['partner_id'] = vals_list['mc_cust']
        return super(mc_kontrak, self).create(vals_list)

    def write(self, vals):
        if self.product_order_line:
            print('hitung subtotal by section')
            subtotal_otf = 0
            subtotal_sub = 0
            print(subtotal_sub, subtotal_otf)

            query = """
                SELECT id FROM mc_kontrak_product_order_line
                WHERE kontrak_id = %s AND display_type = 'line_section'
            """ % self.id
            self.env.cr.execute(query)
            print(query)
            print(self.env.cr.fetchone())
            if self.env.cr.fetchone() is None:
                id_section = 0
            else:
                id_section = self.env.cr.fetchone()[0]

            if id_section != 0:
                query = """
                    SELECT SUM(mc_payment) as subtotal_sub FROM mc_kontrak_product_order_line
                    WHERE id < %s
                """ % id_section
                self.env.cr.execute(query)
                print(query)
                subtotal_sub = self.env.cr.fetchone()[0]
                if subtotal_sub is None:
                    subtotal_sub = 0

                print(subtotal_sub)

                query = """
                    SELECT SUM(mc_payment) as subtotal_otf FROM mc_kontrak_product_order_line
                    WHERE id > %s
                """ % id_section
                self.env.cr.execute(query)
                print(query)
                subtotal_otf = self.env.cr.fetchone()[0]
                if subtotal_otf is None:
                    subtotal_otf = 0

                print(subtotal_otf)

                query = """
                    UPDATE mc_kontrak_mc_kontrak SET x_subtotal_otf = %s,
                    x_subtotal_sub = %s WHERE id = %s
                """ % (subtotal_otf, subtotal_sub, self.id)
                self.env.cr.execute(query)
                print(query)

        return super(mc_kontrak, self).write(vals)

    # def action_sent(self):
    #     query = """
    #         UPDATE mc_kontrak_mc_kontrak SET mc_state = 'sent' WHERE id = %s
    #     """ % self.id
    #     self.env.cr.execute(query)
    #     print("Update kontrak state into Sent")

    # Total Harga
    @api.depends('product_order_line')
    def total_harga(self):
        total = 0.00
        pajak = 0.00
        i = 0
        for rec in self.product_order_line:
            i += 1
            print(i)
            print(rec.mc_pajak)
            total += rec.mc_payment
            pajak += rec.mc_pajak

        print('pajak', pajak)
        self.mc_total = total
        self.mc_pajak = pajak
        self.mc_tak_pajak = total - pajak

    # Hitung berapa SO di Kontrak ini
    def _count_so(self):
        query = "SELECT COUNT(0) FROM public.sale_order where kontrak_id = %s " % self.id
        print(query)
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        self.so_count = result[0]

    # Button untuk membuka related SO
    def action_view_so_button(self):
        action = self.env.ref('sale.action_quotations').read()[0]
        action['domain'] = [('kontrak_id', '=', self.id)]
        action['context'] = {}
        return action

    # Hitung berapa SUBS di Kontrak ini
    def _count_subs(self):
        query = "SELECT COUNT(0) FROM public.sale_subscription where x_kontrak_id = %s " % self.id
        print(query)
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        self.subs_count = result[0]

    # Button untuk membuka related SUBS
    def action_view_subs_button(self):
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sale.subscription",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["x_kontrak_id", "=", self.id]],
            "context": {"create": False},
            "name": "Subscriptions",
        }
        return result

    # Button untuk membuat SO baru dari Kontrak
    def action_create_so_button(self):
        for row in self:
            partner_id = row.mc_cust.id

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'context': {
                'default_partner_id': partner_id,
                'default_kontrak_id': self.id
            }
        }

    def action_confirm(self):
        # Action Confirm Kontrak
        query = """
            UPDATE mc_kontrak_mc_kontrak SET mc_state = 'done', mc_confirm_date = now()
            WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        print('confirm contract')

    def action_cancel(self):
        query = """
            UPDATE mc_kontrak_mc_kontrak SET mc_state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        print('cancel contract')

    @api.depends('product_order_line')
    def _hitung_qty_belum_terpasang(self):
        for row in self.product_order_line:
            query = "SELECT SUM(x_mc_qty_terpasang) FROM public.sale_order_line WHERE kontrak_id = %s AND product_id = %s" % (
                self.id, row.product_id.id)

            self.env.cr.execute(query)
            result = self.env.cr.fetchone()

            print("SUM QTY TERPASANG : ", result[0])
            row.mc_qty_belum_terpasang = row.mc_qty_kontrak - result[0]
            row.mc_qty_terpasang = result[0]


class ProductOrderLine(models.Model):
    _name = 'mc_kontrak.product_order_line'
    _description = 'Order line dari data kontrak'

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string='No Kontrak', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one(
        'product.template', string='Product Template',
        related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])

    currency_id = fields.Many2one('res.currency')
    tax_id = fields.Many2one('account.tax', string='Taxes')

    # Field
    mc_qty_kontrak = fields.Integer(string='QTY Kontrak')
    mc_qty_so = fields.Integer(string='QTY SO')
    mc_qty_terpasang = fields.Integer(string='QTY Terpasang', default=0)
    mc_qty_belum_terpasang = fields.Integer(string='QTY Belum Terpasang')

    mc_harga_produk = fields.Float(string='Standard Price', related='product_template_id.list_price', store=True)
    mc_harga_diskon = fields.Monetary(string='Discounted Price')
    mc_pajak = fields.Float(string='Pajak', compute='_hitung_subtotal', store=True, readonly=True)
    mc_harga_tak_pajak = fields.Monetary(string='Harga Tak Pajak', store=True, readonly=True)

    mc_period = fields.Integer(string='Period')
    mc_period_info = fields.Selection([
        ('bulan', 'Bulan'),
        ('tahun', 'Tahun'),
        ('unit', 'Unit')
    ], string='UoM')
    mc_payment = fields.Float(string='Subtotal', readonly=True, compute='_hitung_subtotal', store=True)
    mc_total = fields.Float(string='Total', readonly=True, store=True)
    mc_isopen = fields.Boolean(default=True)
    mc_unit_price = fields.Monetary(string='Unit Price')

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    name = fields.Char(string='Description', related="product_id.product_tmpl_id.name", store=True)

    @api.depends('mc_qty_kontrak', 'mc_harga_diskon', 'mc_period', 'mc_period_info', 'tax_id')
    def _hitung_subtotal(self):
        subtotal = 0
        grandtotal = 0
        pajakTotalProduk = 0
        totalTakPajak = 0

        for line in self:
            price = 0
            unitPrice = 0
            pajakTotal = pajakUnit = takPajak = 0
            if line.mc_period_info == 'tahun':
                price = line.mc_harga_diskon * line.mc_qty_kontrak * line.mc_period * 12
                unitPrice = line.mc_harga_diskon * line.mc_period * 12
                if line.tax_id:
                    if line.tax_id.amount != 0:
                        takPajak = price
                        pajakTotal = price / (line.tax_id.amount * 100)
                        pajakUnit = unitPrice / (line.tax_id.amount * 100)
            else:
                price = line.mc_harga_diskon * line.mc_qty_kontrak * line.mc_period
                unitPrice = line.mc_harga_diskon * line.mc_period
                if line.tax_id:
                    if line.tax_id.amount != 0:
                        takPajak = price
                        pajakTotal = price / (line.tax_id.amount * 100)
                        pajakUnit = unitPrice / (line.tax_id.amount * 100)

            subtotal += price
            pajakTotalProduk += pajakTotal
            totalTakPajak += takPajak
            line.update({
                'mc_payment': price + pajakTotal,
                'mc_unit_price': unitPrice + pajakUnit,
                'mc_qty_belum_terpasang': line.mc_qty_kontrak
            })

        grandtotal = subtotal
        self.mc_total = grandtotal
        self.mc_pajak = pajakTotalProduk

    @api.model
    def view_init(self, fields_list):
        print(self.display_type)
        print(fields_list)


class CustomSalesOrder(models.Model):
    _inherit = 'sale.order'
    _order = 'kontrak_id DESC'
    _description = 'Modul yang mengcustom module sale.order'

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak', string='No Kontrak', ondelete='cascade')
    kontrak_product_line = fields.Many2one('mc_kontrak.product_order_line')
    histori_wo_line = fields.One2many('mc_kontrak.histori_wo', 'x_order_id')

    wo_count = fields.Integer(string='WO', compute='_count_wo')

    # state = fields.Selection([
    #     ('draft', 'Quotation'),
    #     ('sent', 'Terima DP'),
    #     ('sale', 'Progress'),
    #     ('done', 'Done'),
    #     ('cancel', 'Cancelled'),
    # ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    x_order_line = fields.One2many('sale.order.line', 'order_id')
    x_mc_qty_kontrak = fields.Integer(string='Quantity Kontrak')
    # x_mc_qty_terpasang = fields.Integer(string='Quantity Terpasang')
    # x_mc_harga_produk = fields.Monetary(string='Standard Price')
    x_mc_isopen = fields.Boolean(default=True, store=True)
    x_start_date = fields.Date(string='Start Date')
    x_no_po = fields.Char(string='No PO Customer')
    x_qty_terpasang = fields.Integer(default=0, store=True)

    x_subtotal_otf_so = fields.Monetary(string='Subtotal One Time Fee')
    x_subtotal_sub_so = fields.Monetary(string='Subtotal Subscription')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")

    note = fields.Html(store=True,
                       default='<p><span style=font-weight:bolder>Catatan: </span><br><ol><li>PIHAK KEDUA melakukan pembayaran sejumlah nilai diatas setelah penandatanganan PERJANJIAN. Pemasangan PRODUK oleh PIHAK PERTAMA akan dilakukan 5 (lima) hari setelah dilakukan pembayaran oleh PIHAK KEDUA.<li>Nilai nominal pembayaran di atas belum termasuk PPN.<li>Masa aktif PRODUK terhitung sejak tanggal pemasangan sampai dengan JANGKA WAKTU<li>Apabila pada tanggal jatuh tempo tidak terjadi pembayaran, maka:<ol type=a><li>30 (tiga puluh) hari sejak tanggal jatuh tempo, akses ke sistem akan ditutup<li>60 (enam puluh) hari sejak tanggal jatuh tempo, layanan akan ditutup</ol><li>Pembayaran dapat dilakukan melalui transfer kepada:<table><tr><td><h5>PT Otto Menara Globalindo</h5><tr><td>Bank Central Asia (BCA)<tr><td>KCP Kusuma Bangsa<tr><td>No. Rekening 188.212.6689</table><li>Setelah dilakukannya pembayaran, PIHAK KEDUA wajib mengirimkan bukti pembayaran ke surel <a href=mailto:finance@mceasy.co.id target=_blank>finance@mceasy.co.id</a></ol>')
    subs_count = fields.Integer(string='Subscription', compute='_count_subs')

    # Hitung jumlah subs tiap WO
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        """Compute the number of distinct subscriptions linked to the order."""
        for order in self:
            sub_count = len(
                self.env['sale.order.line'].read_group([('order_id', '=', order.id), ('subscription_id', '!=', False)],
                                                       ['subscription_id'], ['subscription_id']))
            order.subscription_count = sub_count

    @api.model
    def create(self, vals_list):
        print('Akses Method Create Custom Sale Order')
        if 'device_wo_line' in vals_list:
            vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.work_order')
        else:
            vals_list['name'] = self.env['ir.sequence'].next_by_code('sale.order.new')
        return super(CustomSalesOrder, self).create(vals_list)

    def write(self, vals):
        print('method write diakses')
        res = super(CustomSalesOrder, self).write(vals)
        print(self.kontrak_id.id)
        if ('order_line' in vals):
            arr_order_line = vals['order_line']
            print(arr_order_line)

            print('hitung subtotal SO by section')
            subtotal_otf = 0
            subtotal_sub = 0
            print(subtotal_sub, subtotal_otf)

            query = """
                SELECT id FROM sale_order_line
                WHERE order_id = %s AND display_type = 'line_section'
            """ % self.id
            self.env.cr.execute(query)
            print(query)
            hasil_fetch = self.env.cr.fetchone()
            if hasil_fetch is None:
                id_section = 0
            else:
                id_section = hasil_fetch[0]

            print(id_section)
            if id_section != 0:
                query = """
                    SELECT SUM(price_subtotal) as subtotal_sub FROM sale_order_line
                    WHERE id < %s AND order_id = %s
                """ % (id_section, self.id)
                self.env.cr.execute(query)
                print(query)
                subtotal_sub = self.env.cr.fetchone()[0]
                if subtotal_sub is None:
                    subtotal_sub = 0

                print(subtotal_sub)

                query = """
                    SELECT SUM(price_subtotal) as subtotal_otf FROM sale_order_line
                    WHERE id > %s AND order_id = %s
                """ % (id_section, self.id)
                self.env.cr.execute(query)
                print(query)
                subtotal_otf = self.env.cr.fetchone()[0]
                if subtotal_otf is None:
                    subtotal_otf = 0

                print(subtotal_otf)

                query = """
                    UPDATE sale_order SET x_subtotal_otf_so = %s,
                    x_subtotal_sub_so = %s WHERE id = %s
                """ % (subtotal_otf, subtotal_sub, self.id)
                self.env.cr.execute(query)
                print(query)

        return res

    # Auto fill Order Line
    def insert_kontrak(self):
        print('insert kontrak func')
        kontrak_id = self.kontrak_id
        partner = self.partner_id
        terms = []

        kontrak_line = self.env['mc_kontrak.mc_kontrak'].search([('id', '=', kontrak_id.id)])
        subs_id = self.env['sale.subscription'].search([('x_kontrak_id', '=', kontrak_id.id)])

        if kontrak_line:
            for row in kontrak_line.product_order_line:
                values = {}

                # Cek jika status produk open, masukkan ke SO
                if row.mc_isopen:
                    if row.product_id.id:
                        values['product_id'] = row.product_id.id
                        values['name'] = row.name
                        values['kontrak_line_id'] = row.id
                        values['x_mc_qty_kontrak'] = row.mc_qty_kontrak
                        values['kontrak_id'] = kontrak_id.id
                        values['price_unit'] = row.mc_harga_diskon
                        values['discount'] = (row.mc_harga_produk - row.mc_harga_diskon) / row.mc_harga_produk
                        values['x_mc_isopen'] = row.mc_isopen
                        values['product_uom_qty'] = row.mc_qty_kontrak - row.mc_qty_terpasang
                        values['discount'] = 0
                        values['x_mc_harga_produk'] = row.mc_harga_produk
                        if subs_id.id:
                            values['subscription_id'] = subs_id.id

                        terms.append((0, 0, values))

        return self.update({'order_line': terms})

    def action_cancel(self):
        print('test cancel')
        query = """
            SELECT product_uom_qty, kontrak_line_id  FROM sale_order_line sol 
            WHERE sol.order_id  = %s
        """ % self.id

        self.env.cr.execute(query)
        arrQuery = self.env.cr.dictfetchall()

        if arrQuery:
            query = """
                update mc_kontrak_mc_kontrak set mc_isopen = true where id = %s
            """ % self.kontrak_id.id
            self.env.cr.execute(query)
            for row in arrQuery:
                query = """
                    update mc_kontrak_product_order_line set
                    mc_qty_terpasang = mc_qty_belum_terpasang - %s,
                    mc_qty_belum_terpasang = mc_qty_belum_terpasang - %s
                    where id = %s 
                """ % (row['product_uom_qty'], row['product_uom_qty'], row['kontrak_line_id'])
                self.env.cr.execute(query)

        query = """
                UPDATE sale_order SET state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        query = """
            DELETE FROM mc_kontrak_histori_so WHERE x_order_id = %s
        """ % self.id
        self.env.cr.execute(query)

        res = super(CustomSalesOrder, self).action_cancel()
        return res

    def action_confirm(self):
        # Action Confirm SO
        print('action confirm from SO')
        so_line = self.x_order_line
        qty_so = 0

        query = """
            SELECT x_islocked FROM res_partner WHERE id = %s
        """ % self.partner_id.id
        print(query)
        self.env.cr.execute(query)
        is_company_locked = self.env.cr.fetchone()[0]

        if is_company_locked:
            print('Company is Locked')
            text = """Tidak dapat mengkonfirmasi SO. Status Company masih di Lock"""
            query = 'delete from display_dialog_box'
            self.env.cr.execute(query)
            value = self.env['display.dialog.box'].sudo().create({'text': text})
            return {
                'name': 'Company di Lock',
                'type': 'ir.actions.act_window',
                'res_model': 'display.dialog.box',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'res_id': value.id,
                'flags': {'form': {'action_buttons': True}}
            }
        else:
            if self.kontrak_id.id is False:
                # Buat Kontrak Baru dan Ambil IDnya
                contract_name = self.env['ir.sequence'].next_by_code('mc_kontrak.mc_kontrak')
                query = """
                    INSERT INTO mc_kontrak_mc_kontrak(mc_cust, name, mc_create_date, mc_isopen, mc_state,
                    mc_sales, mc_admin_sales, mc_confirm_date, x_kontrak_start_date, x_kontrak_end_date, mc_pic_cust, 
                    company_id, partner_id) VALUES 
                    ('%s', '%s', now(), true, 'draft', '%s', '%s',now(), now(), now() + interval '1 year', (SELECT x_pic
                    FROM res_partner WHERE id = %s), %s, %s)
                    RETURNING id
                """ % (self.partner_id.id, contract_name, self.env.user.id, self.env.user.id, self.partner_id.id,
                       self.env.company.id, self.partner_id.id)
                self.env.cr.execute(query)
                print(query)
                kontrak_id = self.env.cr.fetchone()[0]

                # Cek order_line, masukkan ke product_order_line Kontrak
                if self.x_order_line:
                    for row in self.x_order_line:
                        if row.product_id.product_tmpl_id.recurring_invoice:
                            #     If FALSE
                            #     query = """
                            #         INSERT INTO mc_kontrak_product_order_line(kontrak_id, name, display_type)
                            #         VALUES ('%s', '%s', '%s') RETURNING id
                            #     """ % (kontrak_id, row.name, row.display_type)
                            #     print(query)
                            #     self.env.cr.execute(query)
                            #     result = self.env.cr.dictfetchone()
                            #     id_sol = result['id']
                            # else:
                            self.env.cr.execute("""SELECT * FROM product_template WHERE id = %s""" % row.product_id.id)
                            product_id = self.env.cr.dictfetchone()
                            query = """
                                INSERT INTO mc_kontrak_product_order_line(kontrak_id, product_id, mc_qty_kontrak, 
                                mc_qty_terpasang, mc_harga_produk, mc_harga_diskon, mc_period, mc_period_info, 
                                currency_id, tax_id, mc_isopen, name, mc_payment, mc_total)
                                VALUES ('%s','%s','%s','%s','%s','%s', '1', 'bulan', 12, 1, true, '%s', '%s', '%s') RETURNING id
                            """ % (kontrak_id, row.product_id.id if row.product_id.id else 0, row.x_mc_qty_kontrak,
                                   int(row.product_uom_qty), row.x_mc_harga_produk, row.price_unit, row.name,
                                   row.price_total, row.price_total)
                            print(query)
                            self.env.cr.execute(query)
                            result = self.env.cr.dictfetchone()
                            id_sol = result['id']

                        # Masukkan Sales Order ke histori SO
                        if row.product_id.id:
                            query = """
                                INSERT INTO mc_kontrak_histori_so(x_kontrak_id,
                                x_tgl_start, x_item, x_period,
                                x_note, x_qty_so) VALUES ('%s',now(),'%s','%s','','%s')
                            """ % (kontrak_id, row.product_id.id, '1 - bulan', int(row.product_uom_qty))
                            print(query)
                            self.env.cr.execute(query)

                # Update Sales Order, agar berelasi dengan Kontrak yang baru dibuat
                self.env.cr.execute("SELECT id FROM sale_order ORDER BY id DESC LIMIT 1")
                order_id = self.env.cr.fetchone()[0]
                print(order_id)

                query = """
                    UPDATE sale_order SET kontrak_id = %s WHERE id = %s
                """ % (kontrak_id, order_id)
                print(query)
                self.env.cr.execute(query)

                # Update histori SO agar nyambung Sales Order Id
                query = """
                    UPDATE mc_kontrak_histori_so SET x_order_id = %s WHERE x_kontrak_id = %s
                """ % (order_id, kontrak_id)
                self.env.cr.execute(query)

                # Update Sale Order Line set Kontrak ID
                self.env.cr.execute("""UPDATE sale_order_line SET kontrak_id = %s, kontrak_line_id = %s 
                WHERE order_id = %s""" % (kontrak_id, id_sol, order_id))
            else:
                if so_line:
                    i = 0
                    for row in so_line:
                        # if arr_order_line[i][2]['product_uom_qty']:
                        # x_qty_terpasang = arr_order_line[i][2]['product_uom_qty']
                        id_sol = 0
                        print('row :', row)
                        print('row kontrak line : ', row.kontrak_line_id.id)
                        print('row kontrak line 2 : ', row.kontrak_line_id)
                        if row.kontrak_line_id.id is False and row.product_id.id:
                            print(row.order_id.kontrak_id.mc_qty_kontrak)
                            print(int(row.order_id.kontrak_id.mc_qty_kontrak))

                            query = """
                                INSERT INTO mc_kontrak_product_order_line(kontrak_id, product_id, currency_id,
                                mc_qty_kontrak, mc_qty_terpasang, mc_harga_produk, mc_harga_diskon, mc_payment,
                                mc_total, mc_unit_price) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') RETURNING id
                            """ % (row.kontrak_id.id, row.product_id.id, row.currency_id.id,
                                   int(row.order_id.kontrak_id.mc_qty_kontrak), int(row.product_uom_qty),
                                   row.price_unit,
                                   row.price_unit, row.price_total, row.price_total, row.price_unit)
                            print(query)
                            self.env.cr.execute(query)
                            result = self.env.cr.dictfetchone()
                            id_sol = result['id']

                        query = """
                            SELECT mc_period, mc_period_info FROM mc_kontrak_product_order_line
                            WHERE kontrak_id = %s
                        """ % self.kontrak_id.id
                        print(query)
                        self.env.cr.execute(query)
                        getPeriod = self.env.cr.dictfetchone()
                        periode = str(getPeriod['mc_period']) + " " + str(getPeriod['mc_period_info'])

                        if row.product_id.id:
                            query = """
                                INSERT INTO mc_kontrak_histori_so(x_kontrak_id,
                                x_order_id, x_tgl_start, x_item, x_period, x_status_pembayaran,
                                x_note, x_qty_so) VALUES ('%s','%s',now(),'%s','%s','%s','','%s' )
                            """ % (
                                self.kontrak_id.id, row.order_id.id, row.product_id.id,
                                periode, self.state, int(row.product_uom_qty))
                            print(query)
                            self.env.cr.execute(query)

                        x_qty_terpasang = row.product_uom_qty
                        print('product_uom_qty = ', x_qty_terpasang)

                        query = "SELECT coalesce(SUM(sol.product_uom_qty), 0) FROM public.sale_order so " \
                                "JOIN public.sale_order_line sol " \
                                "ON sol.order_id = so.id " \
                                "WHERE so.state NOT IN('cancel') AND " \
                                "sol.kontrak_line_id = %s AND " \
                                "sol.id != %s" % (
                                    id_sol if row.kontrak_line_id.id is False else row.kontrak_line_id.id, row.id)
                        self.env.cr.execute(query)
                        print(query)
                        x_qty_terpasang2 = self.env.cr.fetchone()[0]
                        total_terpasang = x_qty_terpasang + x_qty_terpasang2

                        query = "UPDATE public.mc_kontrak_product_order_line SET mc_qty_terpasang = %s, " \
                                "mc_qty_belum_terpasang = (mc_qty_kontrak - %s) " \
                                "WHERE id = %s" % (
                                    total_terpasang, total_terpasang, id_sol if row.kontrak_line_id.id is False
                                    else row.kontrak_line_id.id)
                        print(query)
                        self.env.cr.execute(query)

                        query = """
                            UPDATE mc_kontrak_mc_kontrak SET mc_qty_kontrak = %s WHERE id = %s
                        """ % (row.x_mc_qty_kontrak, row.kontrak_id.id)
                        self.env.cr.execute(query)

                        if query:
                            print('oke, qty dikurangi, histori so dimasukkan')
                        i = i + 1

                    query = """
                        update mc_kontrak_mc_kontrak set
                        mc_isopen = False
                        where id = %s
                        and mc_qty_kontrak = (
                            select SUM(mkpol.mc_qty_terpasang) as mc_qty_terpasang
                            from mc_kontrak_mc_kontrak mkmk
                            join mc_kontrak_product_order_line mkpol on mkpol.kontrak_id = mkmk.id
                            where mkmk.id = %s
                        )
                    """ % (self.kontrak_id.id, self.kontrak_id.id)
                    print(query)
                    self.env.cr.execute(query)

                    query = """SELECT SUM(x_qty_so) FROM mc_kontrak_histori_so mkhs WHERE x_kontrak_id = %s""" % self.kontrak_id.id
                    print(query)
                    self.env.cr.execute(query)
                    sum_qty_so = self.env.cr.fetchone()[0]

                    query = """UPDATE mc_kontrak_product_order_line SET mc_qty_terpasang = %s 
                    WHERE kontrak_id = %s AND product_id = %s""" % (sum_qty_so, self.kontrak_id.id, row.product_id.id)
                    print(query)
                    self.env.cr.execute(query)

            query = """
                    UPDATE sale_order SET state = 'sale' WHERE id = %s
            """ % self.id
            self.env.cr.execute(query)

            res = super(CustomSalesOrder, self).action_confirm()
            return res

    # Button untuk membuat WO baru dari SO
    def action_report_wo_spk(self):
        for row in self:
            partner_id = row.kontrak_id.mc_cust.id

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mc_kontrak.work_order',
            'context': {
                'default_partner_id': partner_id,
                'default_kontrak_id': row.kontrak_id.id,
                'default_order_id': self.id
            }
        }

    # Button untuk membuka related WO
    def action_view_wo_button(self):
        action = self.env.ref('mc_kontrak.work_order_course_action').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        action['context'] = {}
        return action

    # Hitung berapa WO di SO ini
    def _count_wo(self):
        self.env.cr.execute("SELECT COUNT(0) FROM public.mc_kontrak_work_order where order_id = %s " % self.id)
        result = self.env.cr.fetchone()
        self.wo_count = result[0]

    # Hitung berapa SUBS di SO ini
    def _count_subs(self):
        query = "SELECT COUNT(0) FROM public.sale_subscription where x_kontrak_id = %s " % self.kontrak_id.id
        print(query)
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        self.subs_count = result[0]

    # Button untuk membuka related SUBS
    def action_view_subs_button(self):
        action = self.env.ref('sale_subscription.sale_subscription_action').read()[0]
        action['domain'] = [('x_kontrak_id', '=', self.id)]
        action['context'] = {}
        return action


class CustomSalesOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Modul yang mengcustom module sale.order.line'

    product_id = fields.Many2one('product.product')
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak')
    kontrak_line_id = fields.Many2one('mc_kontrak.product_order_line')

    # Field
    x_mc_qty_kontrak = fields.Integer(string='QTY Kontrak', store=True)
    x_mc_qty_terpasang = fields.Integer(readonly=True, store=True)
    x_mc_harga_produk = fields.Float(string='Standard Price', store=True)
    x_mc_harga_diskon = fields.Monetary()
    x_mc_isopen = fields.Boolean(default=True, store=True)

    # price_subtotal = fields.Monetary(compute='_hitung_subtotal_so')

    @api.onchange('product_id')
    def _get_unit_price(self):
        if self.product_id:
            self.env.cr.execute("""SELECT product_tmpl_id FROM product_product WHERE id = %s""" % self.product_id.id)
            product_tmpl_id = self.env.cr.fetchone()[0]
            if product_tmpl_id:
                self.env.cr.execute("""SELECT list_price FROM product_template WHERE id = %s""" % product_tmpl_id)
                list_price = self.env.cr.fetchone()[0]
                self.x_mc_harga_produk = list_price

    # Total Harga
    @api.depends('x_mc_harga_produk', 'x_mc_harga_diskon', 'x_mc_qty_terpasang')
    def _hitung_subtotal_so(self):
        subtotal = 0

        for line in self:
            price = line.x_mc_harga_diskon * line.x_mc_qty_terpasang
            print('price in row ', price)
            subtotal += price
            line.update({
                'price_subtotal': price
            })


class WorkOrder(models.Model):
    _name = 'mc_kontrak.work_order'
    _inherit = 'sale.order'
    _description = 'Modul Work Order yang menginherit sale.order'

    # Field
    name = fields.Char(string='No WO', readonly=True, default='New')
    x_teknisi_1 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string="Teknisi 1", required=True)
    x_teknisi_2 = fields.Many2one('res.partner',
                                  domain="[('function', '=', 'Teknisi McEasy')]", string='Teknisi 2')

    x_created_date = fields.Date(default=fields.Datetime.now(), string='Created Date')
    x_sales = fields.Many2one('res.users', string='Admin', default=lambda self: self.env.user, readonly=True)
    x_isopen = fields.Boolean(default=True, store=True)
    x_plan_start_date = fields.Datetime(store=True)
    x_plan_end_date = fields.Datetime(store=True)

    # Relasi
    kontrak_id = fields.Many2one('mc_kontrak.mc_kontrak')
    order_id = fields.Many2one('sale.order', store=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', related='kontrak_id.mc_cust', store=True)
    product_id = fields.Many2one('product.product')
    work_order_line = fields.One2many('mc_kontrak.work_order_line', 'work_order_id', store=True)
    device_wo_line = fields.One2many('mc_kontrak.device_wo', 'x_work_order_id', string='Device WO', store=True,
                                     ondelete='cascade')

    # Relasi dari sale.order
    transaction_ids = fields.Many2many('payment.transaction', 'work_order_transaction_rel', 'id',
                                       'transaction_id',
                                       string='Transactions', copy=False, readonly=True)
    tag_ids = fields.Many2many('crm.tag', 'work_order_tag_rel', 'id', 'tag_id', string='Tags')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'In Progress'),
        ('sale', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', copy=False, index=True, tracking=3, default='draft')

    # Hitung jumlah subs tiap WO
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        """Compute the number of distinct subscriptions linked to the order."""
        for order in self:
            sub_count = len(
                self.env['mc_kontrak.work_order_line'].read_group(
                    [('work_order_id', '=', order.id), ('subscription_id', '!=', False)],
                    ['subscription_id'], ['subscription_id']))
            order.subscription_count = sub_count

    def action_open_subscriptions(self):
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sale.subscription",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["x_kontrak_id", "=", self.kontrak_id.id]],
            "context": {"create": False},
            "name": "Subscriptions",
        }
        return result

    @api.model
    def create(self, vals_list):
        print('Halo dari Work Order')
        res = super(WorkOrder, self).create(vals_list)
        print(vals_list)
        vals_list['name'] = self.env['ir.sequence'].next_by_code('mc_kontrak.work_order')
        return res

    def write(self, vals):
        res = super(WorkOrder, self).write(vals)
        device_wo_line = self.device_wo_line
        if device_wo_line:
            for row in device_wo_line:
                query = """
                    UPDATE mc_kontrak_device_wo SET x_partner_id = %s
                """ % row.x_work_order_id.partner_id.id
                self.env.cr.execute(query)

                query = """
                    SELECT COUNT(id) FROM mc_kontrak_device_wo WHERE x_work_order_id = %s 
                """ % self.id
                self.env.cr.execute(query)
                count_device_terpasang = self.env.cr.fetchone()[0]

                query = """
                    UPDATE mc_kontrak_work_order_line SET qty_delivered = %s WHERE work_order_id = %s
                """ % (count_device_terpasang, self.id)
                self.env.cr.execute(query)

        return res

    # Auto fill Work Order Line
    def insert_so_line(self):
        print('insert SO line func')
        kontrak_id = self.kontrak_id.id
        order_id = self.order_id.id
        terms = []
        print(order_id)
        so_line = self.env['sale.order'].search([('id', '=', order_id)])
        print(so_line)
        if so_line:
            for row in so_line.order_line:
                values = {}
                if row.product_id.product_tmpl_id.recurring_invoice:
                    # Cek jika status produk open, masukkan ke WO Line
                    values['product_id'] = row.product_id.id
                    values['order_id'] = row.order_id.id
                    values['product_uom_qty'] = row.product_uom_qty
                    values['x_qty_plan'] = row.product_uom_qty
                    values['sale_order_line_id'] = row.id
                    values['price_unit'] = row.price_unit
                    values['name'] = row.name
                    # else:
                    #     values['name'] = row.name
                    #     values['display_type'] = row.display_type
                    #     values['sale_order_line_id'] = row.id

                    terms.append((0, 0, values))

        return self.update({'work_order_line': terms})

    def action_cancel(self):
        print('test cancel work order')
        query = """
            SELECT qty_delivered, sale_order_line_id  FROM mc_kontrak_work_order_line wol 
            WHERE wol.work_order_id  = %s
        """ % self.id
        self.env.cr.execute(query)
        print(query)
        arrQuery = self.env.cr.dictfetchall()
        print(arrQuery)

        if arrQuery:
            query = """
                update sale_order set x_mc_isopen = true where id = %s
            """ % self.kontrak_id.id
            self.env.cr.execute(query)
            for row in arrQuery:
                query = """
                    update sale_order_line set
                    qty_delivered = qty_delivered - %s
                    where id = %s 
                """ % (row['qty_delivered'], row['sale_order_line_id'])
                print(query)
                self.env.cr.execute(query)

        query = """
            DELETE FROM mc_kontrak_histori_wo WHERE x_work_order_id = %s
        """ % self.id
        self.env.cr.execute(query)

        query = """
                UPDATE mc_kontrak_work_order SET state = 'cancel' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)

        res = super(WorkOrder, self).action_cancel()
        return res

    def action_confirm(self):
        print('action confirm tes work order')
        wo_line = self.work_order_line
        if wo_line:
            i = 0
            for row in wo_line:
                qty_wo = row.qty_delivered
                print('QTY WO Terpasang = ', qty_wo)

                query = "SELECT coalesce(SUM(wol.qty_delivered), 0) FROM mc_kontrak_work_order wo " \
                        "JOIN mc_kontrak_work_order_line wol " \
                        "ON wol.work_order_id = wo.id " \
                        "WHERE wo.state NOT IN('cancel') AND " \
                        "wol.order_id = %s AND " \
                        "wol.id != %s" % (row.order_id.id, row.id)
                self.env.cr.execute(query)
                print(query)
                x_qty_terpasang2 = self.env.cr.fetchone()[0]
                total_terpasang = qty_wo + x_qty_terpasang2

                query = "UPDATE sale_order_line SET qty_delivered = %s, " \
                        "x_mc_qty_terpasang = %s " \
                        "WHERE id = %s" % (total_terpasang, total_terpasang, row.sale_order_line_id.id)
                self.env.cr.execute(query)

                query = """
                    UPDATE sale_order SET x_qty_terpasang = %s WHERE id = %s
                """ % (row.product_uom_qty, row.order_id.id)
                self.env.cr.execute(query)

                # Memasukkan Histori WO
                query = """
                    INSERT INTO mc_kontrak_histori_wo(x_qty_terpasang,x_date_created,x_work_order_id,x_order_id,
                    x_teknisi_1,x_teknisi_2,x_admin_sales) VALUES ('%s','%s','%s','%s','%s','%s','%s')
                """ % (row.qty_delivered, self.x_created_date, row.work_order_id.id, row.order_id.id,
                       self.x_teknisi_1.id,
                       self.x_teknisi_2.id if self.x_teknisi_2.id is not False else self.x_teknisi_1.id,
                       self.x_sales.id)
                self.env.cr.execute(query)

                print(query)
                print('Histori WO dimasukkan')

                i = i + 1

            query = """
                update sale_order set
                x_mc_isopen = False
                where id = %s
                and x_qty_terpasang = (
                    select SUM(sol.qty_delivered) as terpasang
                    from sale_order so
                    join sale_order_line sol on sol.order_id = so.id
                    where so.id = %s
                )
            """ % (self.order_id.id, self.order_id.id)
            print(query)
            self.env.cr.execute(query)

            query = """
                    UPDATE mc_kontrak_work_order SET state = 'done' WHERE id = %s
            """ % self.id
            self.env.cr.execute(query)

            self.env.cr.execute("""
                SELECT COUNT(id) FROM sale_subscription WHERE x_kontrak_id = %s
            """ % self.kontrak_id.id)
            count_kontrak_on_sub = self.env.cr.fetchone()[0]
            if count_kontrak_on_sub < 1:
                subs_id = self.create_subscriptions()
                query = """
                    UPDATE sale_subscription SET x_kontrak_id = %s, x_order_id = %s WHERE id = %s
                """ % (self.kontrak_id.id, self.order_id.id, subs_id[0])
                self.env.cr.execute(query)

                query = """
                    UPDATE sale_subscription_line SET x_order_id = %s WHERE analytic_account_id = %s
                """ % (self.order_id.id, subs_id[0])
                self.env.cr.execute(query)

                query = """
                    UPDATE sale_order_line SET subscription_id = %s WHERE order_id = %s
                """ % (subs_id[0], self.order_id.id)
                self.env.cr.execute(query)
            else:
                self.env.cr.execute("""
                    SELECT * FROM sale_subscription WHERE x_kontrak_id = %s
                """ % self.kontrak_id.id)
                subs_data = self.env.cr.dictfetchone()
                print(subs_data)
                self.create_line_subscriptions(subs_data, row)

            res = super(WorkOrder, self).action_confirm()
            return res

    def action_sent(self):
        query = """
            UPDATE mc_kontrak_work_order SET state = 'sent' WHERE id = %s
        """ % self.id
        self.env.cr.execute(query)
        print('Update Work Order state to Sent')

    def _siapkan_subs_data(self, template):
        """Prepare a dictionnary of values to create a subscription from a template."""
        self.ensure_one()
        date_today = fields.Date.context_today(self)
        recurring_invoice_day = date_today.day
        recurring_next_date = self.env['sale.subscription']._get_recurring_next_date(
            template.recurring_rule_type, template.recurring_interval,
            date_today, recurring_invoice_day
        )
        values = {
            'name': template.name,
            'template_id': template.id,
            'partner_id': self.partner_id.id,
            'partner_invoice_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'payment_term_id': self.payment_term_id.id,
            'date_start': fields.Date.context_today(self),
            'description': self.note if not is_html_empty(self.note) else template.description,
            'pricelist_id': self.pricelist_id.id,
            'company_id': self.company_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'recurring_next_date': recurring_next_date,
            'recurring_invoice_day': recurring_invoice_day,
            'payment_token_id': self.transaction_ids._get_last().token_id.id if template.payment_mode == 'success_payment' else False,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
        }
        default_stage = self.env['sale.subscription.stage'].search([('category', '=', 'progress')], limit=1)
        if default_stage:
            values['stage_id'] = default_stage.id
        return values

    def create_line_subscriptions(self, subs_data, wo_line):
        for order in self:
            to_create = order._bagi_sub_line()
            for template in to_create:
                values = order._siapkan_subs_data(template)
                values['recurring_invoice_line_ids'] = to_create[template]._siapkan_subs_line_data()
                to_create[template].write({'subscription_id': subs_data['id']})

                self.env['sale.subscription.log'].sudo().create({
                    'subscription_id': subs_data['id'],
                    'event_date': fields.Date.context_today(self),
                    'event_type': '0_creation',
                    'amount_signed': wo_line.price_unit * wo_line.qty_delivered,
                    'recurring_monthly': wo_line.price_unit * wo_line.qty_delivered,
                    'currency_id': 12,
                    'category': subs_data['stage_category'],
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                })

                self.env['sale.subscription.line'].sudo().create({
                    'product_id': wo_line.product_id.id,
                    'analytic_account_id': subs_data['id'],
                    'company_id': wo_line.company_id.id,
                    'name': wo_line.name,
                    'quantity': wo_line.qty_delivered,
                    'uom_id': wo_line.product_id.product_tmpl_id.uom_id.id,
                    'price_unit': wo_line.price_unit,
                    'price_subtotal': wo_line.price_unit * wo_line.qty_delivered,
                    'currency_id': wo_line.currency_id.id,
                    'x_order_id': wo_line.order_id.id
                })

    def create_subscriptions(self):
        """
        Create subscriptions based on the products' subscription template.

        Create subscriptions based on the templates found on order lines' products. Note that only
        lines not already linked to a subscription are processed; one subscription is created per
        distinct subscription template found.

        :rtype: list(integer)
        :return: ids of newly create subscriptions
        """
        res = []
        for order in self:
            to_create = order._bagi_sub_line()
            # create a subscription for each template with all the necessary lines
            for template in to_create:
                values = order._siapkan_subs_data(template)
                values['recurring_invoice_line_ids'] = to_create[template]._siapkan_subs_line_data()
                subscription = self.env['sale.subscription'].sudo().create(values)
                subscription.onchange_date_start()
                res.append(subscription.id)
                to_create[template].write({'subscription_id': subscription.id})
                subscription.message_post_with_view(
                    'mail.message_origin_link', values={'self': subscription, 'origin': order},
                    subtype_id=self.env.ref('mail.mt_note').id, author_id=self.env.user.partner_id.id
                )
                self.env['sale.subscription.log'].sudo().create({
                    'subscription_id': subscription.id,
                    'event_date': fields.Date.context_today(self),
                    'event_type': '0_creation',
                    'amount_signed': subscription.recurring_monthly,
                    'recurring_monthly': subscription.recurring_monthly,
                    'currency_id': subscription.currency_id.id,
                    'category': subscription.stage_category,
                    'user_id': order.user_id.id,
                    'team_id': order.team_id.id,
                })
        return res

    def _bagi_sub_line(self):
        """Split the order line according to subscription templates that must be created."""
        self.ensure_one()
        res = dict()
        new_sub_lines = self.work_order_line.filtered(lambda
                                                          l: not l.subscription_id and l.product_id.subscription_template_id and l.product_id.recurring_invoice)
        templates = new_sub_lines.mapped('product_id').mapped('subscription_template_id')
        for template in templates:
            lines = self.work_order_line.filtered(
                lambda l: l.product_id.subscription_template_id == template and l.product_id.recurring_invoice)
            res[template] = lines
        return res


class WorkOrderLine(models.Model):
    _name = 'mc_kontrak.work_order_line'
    _inherit = 'sale.order.line'
    _description = 'Modul Work Order Line yang menginherit sale.order.line'

    # Relasi
    order_id = fields.Many2one('sale.order', required=True, Store=True, Index=True)
    product_id = fields.Many2one('product.product', readonly=True, store=True)
    invoice_lines = fields.Many2many('account.move.line', 'work_order_line_invoice_rel', 'order_line_id',
                                     'invoice_line_id', string='Invoice Lines', copy=False)
    work_order_id = fields.Many2one('mc_kontrak.work_order', readonly=True, store=True)
    sale_order_line_id = fields.Many2one('sale.order.line', store=True)

    # Field
    qty_delivered = fields.Integer(string='QTY Terpasang')
    x_start_date = fields.Datetime(string='Plan Start Date', store=True)
    x_end_date = fields.Datetime(string='Plan End Date', store=True)
    x_qty_plan = fields.Integer(string="QTY Plan Pasang", store=True)

    # x_start_date_real = fields.Date(string='Real Start Date', store=True)
    # x_end_date_real = fields.Date(string='Real End Date', store=True)

    def _siapkan_subs_line_data(self):
        """Prepare a dictionnary of values to add lines to a subscription."""
        values = list()
        for line in self:
            values.append((0, False, {
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.qty_delivered,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount if line.order_id.subscription_management != 'upsell' else False,
            }))
        return values

    # @api.model
    # def create(self, vals):
    #     print('Action Create dari WO Line')
    #     for row in self:
    #         self.env.cr.execute("""UPDATE mc_kontrak_work_order SET x_plan_start_date = '%s', x_plan_end_date = '%s'
    #                 WHERE id = %s """ % (vals['x_start_date'], vals['x_end_date'], row.work_order_id.id))
    #     res = super(WorkOrderLine, self).create(vals)
    #     return res

    def write(self, vals):
        print('Action Write dari WO Line')
        if 'x_start_date' in vals:
            for row in self:
                self.env.cr.execute("""UPDATE mc_kontrak_work_order SET x_plan_start_date = '%s', x_plan_end_date = '%s'
                        WHERE id = %s """ % (vals['x_start_date'], vals['x_end_date'], row.work_order_id.id))
        res = super(WorkOrderLine, self).write(vals)
        return res
