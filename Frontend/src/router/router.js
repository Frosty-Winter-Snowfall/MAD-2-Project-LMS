import '@fortawesome/fontawesome-free/css/all.css';
import { createRouter, createWebHistory } from 'vue-router';
import LoginOrSignup from '../components/LoginOrSignup.vue';
import UserLogin from '../components/UserLogin.vue';
import TestPage from '../components/Test.vue'
import UserSignup from '../components/UserSignup.vue'
import UserDashboard from '../components/UserDashboard.vue'
import LibrarianLogin from '../components/LibrarianLogin.vue'
import LibrarianDashboard from '../components/LibrarianDashboard.vue'
import AddBooks from '../components/AddBooks.vue'
import AddSections from '../components/AddSections.vue'
import AddBookstos from '../components/AddBookstos.vue'
import SectionManagement from '../components/SectionManagement.vue'
import EditSections from '../components/EditSections.vue'
import BookManagement from '../components/BookManagement.vue'
import EditBooks from '../components/EditBooks.vue'
import RemoveBookSection from '../components/RemoveBooksfroms.vue'
import BorrowBooks from '../components/BorrowBooks.vue'
import UserManagement from '../components/UserManagement.vue'
import IssueRevoke from '../components/IssueRevoke.vue'
import MyBooks from '../components/MyBooks.vue'
import ViewFeedback from '../components/ViewFeedback.vue'
import ViewStatistics from '../components/Statistics.vue'

const routes=[
        {path:'/',component:LoginOrSignup},
        {path:'/ulogin',component:UserLogin},
        {path:'/test',component:TestPage},
        {path:'/usignup',component:UserSignup},
        {path:'/udashboard/:id/:username',component:UserDashboard,props:true},
        {path:'/llogin',component:LibrarianLogin}, 
        {path:'/ldashboard/:id/:username',component:LibrarianDashboard,props:true},
        {path:'/addbooks',component:AddBooks,props: route => ({ id: route.query.id, username: route.query.username }) }, 
        {path:'/addsections',component:AddSections,props: route => ({ id: route.query.id, username: route.query.username }) }, 
        {path:'/addbookstos',component:AddBookstos,props: route => ({ id: route.query.id, username: route.query.username }) },
        {path:'/sectionmanagement',component:SectionManagement,props: route => ({ id: route.query.id, username: route.query.username }) },
        {path: '/editsections/:sectionId', 
        component: EditSections, 
        props: route => ({ 
          sectionId: route.params.sectionId, 
          id: route.query.id, 
          username: route.query.username 
        }) 
      },
      {path:'/bookmanagement',component:BookManagement,props: route => ({ id: route.query.id, username: route.query.username }) },
      {path: '/editbooks/:bookId', 
        component: EditBooks, 
        props: route => ({ 
          bookId: route.params.bookId, 
          id: route.query.id, 
          username: route.query.username 
        }) 
      },
      {path:'/removebooksfroms',component:RemoveBookSection,props: route => ({ id: route.query.id, username: route.query.username }) },
      { path: '/borrowbooks', component: BorrowBooks, props: route => ({ 
        bookId: route.query.bookId, 
        id: route.query.id, 
        username: route.query.username 
      }) },
      {path:'/usermanagement',component:UserManagement,props: route => ({ id: route.query.id, username: route.query.username }) },
      {path: '/issuerevoke', 
        component: IssueRevoke, 
        props: route => ({ 
          
          id: route.query.id, 
          username: route.query.username 
        }) 
      },
      {path:'/mybooks/:id',component:MyBooks,
      props: true},
      {path:'/viewfeedback',component:ViewFeedback,props: route => ({ 
          
        id: route.query.id, 
        username: route.query.username 
      })},
      {path:'/statistics',component:ViewStatistics,props: route => ({ 
          
        id: route.query.id, 
        username: route.query.username 
      })}
    ];
    
    const router=createRouter({
        history: createWebHistory(),
        routes
    });

export default router
    