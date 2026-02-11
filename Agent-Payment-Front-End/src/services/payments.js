import api from "./api";

export const getPayments = () => api.get("/payments/");
export const createPayment = (data) => {
  // Ensure data has all required fields
  const paymentData = {
    ...data,
    payment_date: data.payment_date || new Date().toISOString().split('T')[0]
  };
  return api.post("/payments/", paymentData);
};