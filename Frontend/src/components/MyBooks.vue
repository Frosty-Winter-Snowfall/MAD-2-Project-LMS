<template>
  <div class="kale">
    <!-- Sidebar -->
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
        <span v-if="isCollapsed" class="sr-only">Expand</span>
        <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
      <li>No items to display</li>
      </ul>
    </div>
  
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">My Books</h1>
    </div>

    <!-- Main Content -->
    <div class="main-content" :class="{ animate: animateElements }" role="main">
    <div class="mbinfo-block" :class="{ animate: animateElements }">
      <h1>My Books</h1>
      <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
      <ul>
        <li v-for="book in books" :key="book.book_id">
          <h3>{{ book.book_name }}</h3>
          <p>Date Issued: {{ book.date_issued }}</p>
          <p>Return Date: {{ book.return_date }}</p>
          <div class="button-group">
            <button class="read-button" @click="readBook(book.nid)">Read</button>
            <button class="delete-button" @click="returnBook(book.nid)">Return</button>
            <button class="edit-button" @click="showFeedbackModal(book.nid, book.book_name)">Give your Rating</button>
          </div>
        </li>
      </ul>
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="showModal = false">&times;</span>
          <h2>Give Ratings for {{ currentBookName }}</h2>
          <textarea v-model="feedback" placeholder="Enter your Rating"></textarea>
          <button class="edit-button" @click="submitFeedback">Submit Rating</button>
        </div>
      </div>
    </div>
    </div>
    <!-- Footer -->
    <div class="footer" :class="{ animate: animateElements }">
      <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MyBooks',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      animateElements: false,
      logo: require('@/assets/logo.jpg'),
      books: [],
      message: '',
      success: false,
      showModal: false,
      feedback: '',
      currentBookId: null,
      currentBookName: ''
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchMyBooks();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async fetchMyBooks() {
      try {
        const response = await axios.get(`http://localhost:5000/mybooks/${this.id}`);
        console.log('Books response:', response.data); 
        this.books = response.data.borrowed_books; 
      } catch (error) {
        console.error('No Borrowed books:', error);
        this.message = 'No Borrowed Books';
        this.success = false;
      }
    },
    async readBook(nid) {
  try {
    const response = await axios.get(`http://localhost:5000/read_book/${nid}`, {
      responseType: 'blob' // Ensure response is treated as binary
    });
    if (response.status === 403) {
      console.log('Book revoked due to overdue');
      alert('This book has been revoked due to being overdue.');
      return;
    }
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const url = window.URL.createObjectURL(blob);
    window.open(url);
  } catch (error) {
    console.error('Error reading book:', error);
    if (error.response && error.response.status === 403) {
      alert('This book has been revoked due to being overdue.');
    } else {
      alert('Error reading book.');
    }
  }
},


    async returnBook(nid) {
      try {
        await axios.post(`http://localhost:5000/return_book/${nid}`);
        this.message = 'Book returned successfully';
        this.success = true;
        location.reload();
      } catch (error) {
        console.error('Error returning book:', error);
        this.message = 'Error returning book';
        this.success = false;
      }
    },
    showFeedbackModal(bookId, bookName) {
      this.currentBookId = bookId;
      this.currentBookName = bookName;
      this.showModal = true;
    },
    async submitFeedback() {
      try {
        await axios.post(`http://localhost:5000/feedback/${this.currentBookId}`, {
          feedback_content: this.feedback
        });
        this.message = 'Ratings submitted successfully';
        this.success = true;
        this.showModal = false;
        this.feedback = '';
        this.fetchMyBooks();
      } catch (error) {
        console.error('Error submitting Rating:', error);
        this.message = 'Error submitting Rating';
        this.success = false;
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
.read-button {
  background-color: #4cd767; /* Pink color */
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.read-button:hover {
  background-color: #55D0FF; /* Darker shade of pink on hover */
}
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.mbinfo-block {
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

.mbinfo-block.animate {
  opacity: 1;
  transform: translateY(0);
}
</style>
