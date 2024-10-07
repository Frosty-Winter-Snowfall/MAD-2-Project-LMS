<template>
  <div class="libd">
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
        <span v-if="isCollapsed" class="sr-only">Expand</span>
        <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
        <li><router-link :to="`/ldashboard/${id}/${username}`">Dashboard</router-link></li>
        <li><router-link :to="{ path: '/bookmanagement', query: { id: id, username: username } }">Book Management</router-link></li>
        <li><router-link :to="{ path: '/sectionmanagement', query: { id: id, username: username } }">Section Management</router-link></li>
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Manage Users</h1>
    </div>


    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="irinfo-block" :class="{ animate: animateElements }">
        <h1>Issue/Revoke Books to Users</h1>
        <div v-if="notifications.length">
          <table>
            <thead>
              <tr>
                <th>NID</th>
                <th>Consumer Name</th>
                <th>Book Name</th>
                <th>Date Issued</th>
                <th>Return Date</th>
                <th>Returned Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="notification in notifications" :key="notification.nid">
                <td>{{ notification.nid }}</td>
                <td>{{ notification.consumer_name }}</td>
                <td>{{ notification.book_name }}</td>
                <td>{{ notification.date_issued }}</td>
                <td>{{ notification.return_date }}</td>
                <td>{{ notification.is_returned ? notification.returned_date : 'Not Returned' }}</td>
                <td>
                <div class="button-group">
                  <button v-if="!notification.is_returned" class="edit-button" @click="processNotification(notification.nid)">Approve</button>
                    <button v-if="notification.is_returned" class="edit-button" disabled>Returned</button>
                    <button class="delete-button" @click="ignoreNotification(notification.nid)">Ignore</button>
                <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
                  {{ message }}
                </div>
                </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <p>No pending notifications.</p>
        </div>
      </div>
      
    </div>
    <div class="footer" :class="{ animate: animateElements }">
      <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'IssueRevoke',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      notifications: [],
      success: false
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchNotifications();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async fetchNotifications() {
      try {
        const response = await axios.get('http://localhost:5000/notifications');
        this.notifications = response.data;
      } catch (error) {
        console.error('Error fetching notifs:', error);
      }
    },
    async processNotification(nid) {
      try {
        const response = await axios.post(`http://localhost:5000/process_notification/${nid}`);
        this.message = 'Notification approved successfully!';
        this.fetchNotifications();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        console.error('Error approving notification:', error);
        this.message = 'Error approving.';
        this.success=false;
      }
    },
    async ignoreNotification(nid) {
        try{
        const response = await axios.post(`http://localhost:5000/ignore_notification/${nid}`)
        this.message = 'Notification ignored successfully!';
        this.fetchNotifications();
        this.message = response.data.message;
        this.success = true;
        }
         catch(error)  {
          console.error('Error ignoring notification:', error);
          this.message = 'Error.';
          this.success=false;
        }
        
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
  }
};
</script>


<style>
.irinfo-block {
  max-height: 444px;
  width: 95%; 
  margin: 10px 0;
  background: #f0f0f0b0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
  overflow-y: auto;
}

.irinfo-block.animate {
  opacity: 1;
  transform: translateY(0);
}
.irinfo-block input {
  width: 100%;
  margin-bottom: 10px;
}

.irinfo-block ul {
  
  padding: 0;
}

.irinfo-block li {
    margin-left: 50px;
    margin-bottom: 10px;
}
.irinfo-block h3 {
  margin-top: 0;
}
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px 12px;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
}

button {
  margin: 0 5px;
}
</style>
