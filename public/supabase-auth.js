import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

const SUPABASE_URL = 'https://pecfzooycluiocazltgc.supabase.co'
const SUPABASE_KEY = 'sb_publishable_npE5f-0b_qQONBcGs6nRSA_KQLfOL9Z'

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

document.addEventListener('submit', async function (event) {
  const form = event.target

  if (form.id !== 'loginForm' && form.id !== 'signupForm') {
    return
  }

  event.preventDefault()
  event.stopImmediatePropagation()

  const email = form.querySelector('input[type="email"]')?.value.trim()
  const password = form.querySelector('input[type="password"]')?.value

  if (!email || !password) {
    alert('Email and password are required.')
    return
  }

  if (form.id === 'signupForm') {
    const { error } = await supabase.auth.signUp({
      email,
      password
    })

    if (error) {
      alert(error.message)
      return
    }

    alert('Account created successfully. Please check your email to verify your account.')
    return
  }

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) {
    alert(error.message)
    return
  }

  alert('Login successful.')
}, true)