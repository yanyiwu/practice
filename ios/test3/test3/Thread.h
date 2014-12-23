#ifndef XCOMET_THREAD_H
#define XCOMET_THREAD_H

#include <assert.h>
#include <pthread.h>

namespace Xcomet
{
    class IThread
    {
        private:
            pthread_t thread_;
            bool isStarted;
            bool isJoined;
        public:
            IThread(): isStarted(false), isJoined(false)
            {
            }
            virtual ~IThread()
            {
                if(isStarted && !isJoined)
                {
                    assert(!pthread_detach(thread_));
                }
            };
        public:
            virtual void run() = 0;
            void start()
            {
                assert(!isStarted);
                assert(!pthread_create(&thread_, NULL, worker_, this));
                isStarted = true;
            }
            void join()
            {
                assert(!isJoined);
                assert(!pthread_join(thread_, NULL));
                isJoined = true;
            }
        private:
            static void * worker_(void * data)
            {
                IThread * ptr = (IThread* ) data;
                ptr->run();
                return NULL;
            }
    };
} // namespace Xcomet

#endif
