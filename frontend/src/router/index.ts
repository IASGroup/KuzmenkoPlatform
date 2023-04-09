import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BondarenkoView from "@/views/fios/bondarenko/BondarenkoView.vue";
import BabayevView from "@/views/fios/babayev/BabayevView.vue";
import VasilievView from "@/views/fios/vasiliev/VasilievView.vue";
import GulakView from "@/views/fios/gulak/GulakView.vue";
import IvaninView from "@/views/fios/ivanin/IvaninView.vue";
import KolotvinView from "@/views/fios/kolotvin/KolotvinView.vue";
import LevkinView from "@/views/fios/levkin/LevkinView.vue";
import LisovskyView from "@/views/fios/lisovsky/LisovskyView.vue";
import PozdnyakovView from "@/views/fios/pozdnyakov/PozdnyakovView.vue";
import RoopseyView from "@/views/fios/roopsey/RoopseyView.vue";
import SavenkovView from "@/views/fios/savenkov/SavenkovView.vue";
import SmirnovView from "@/views/fios/smirnov/SmirnovView.vue";
import StuzhnyView from "@/views/fios/stuzhny/StuzhnyView.vue";
import SunnitsaView from "@/views/fios/sunnitsa/SunnitsaView.vue";
import TolkachevView from "@/views/fios/tolkachev/TolkachevView.vue";
import TelepnevView from "@/views/fios/telepnev/TelepnevView.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/bondarenko',
        name: 'bondarenko',
        component: BondarenkoView
    },
    {
        path: '/babayev',
        name: 'Babayev',
        component: BabayevView
    },
    {
        path: '/vasiliev',
        name: 'Vasiliev',
        component: VasilievView
    },
    {
        path: '/gulak',
        name: 'Gulak',
        component: GulakView
    },
    {
        path: '/ivanin',
        name: 'Ivanin',
        component: IvaninView
    },
    {
        path: '/kolotvin',
        name: 'Kolotvin',
        component: KolotvinView
    },
    {
        path: '/levkin',
        name: 'Levkin',
        component: LevkinView
    },
    {
        path: '/lisovsky',
        name: 'Lisovsky',
        component: LisovskyView
    },
    {
        path: '/pozdnyakov',
        name: 'Pozdnyakov',
        component: PozdnyakovView
    },
    {
        path: '/roopsey',
        name: 'Roopsey',
        component: RoopseyView
    },
    {
        path: '/savenkov',
        name: 'Savenkov',
        component: SavenkovView
    },
    {
        path: '/smirnov',
        name: 'Smirnov',
        component: SmirnovView
    },
    {
        path: '/stuzhny',
        name: 'Stuzhny',
        component: StuzhnyView
    },
    {
        path: '/sunnitsa',
        name: 'Sunnitsa',
        component: SunnitsaView
    },
    {
        path: '/tolkachev',
        name: 'Tolkachev',
        component: TolkachevView
    },
    {
        path: '/telepnev',
        name: 'Telepnev',
        component: TelepnevView
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
