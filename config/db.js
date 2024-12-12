import { connect } from 'mongoose';

const connectDB = async () => {
    try {
        await connect('mongodb+srv://yodaheketema:1955yyy4@students.k7ooi.mongodb.net/', {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        console.log('MongoDB connected');
    } catch (err) {
        console.error(err.message);
        process.exit(1);
    }
};

export default connectDB;
